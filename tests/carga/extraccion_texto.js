// Prueba de carga con k6: velocidad de extracción de texto del monolito.
//
// Cada iteración genera un PDF con texto (único, para no chocar con la regla
// de duplicados por checksum), lo sube a POST /api/v1/pdfs/, registra el
// header X-Extraction-Time-Ms y después lo borra para no llenar la base.
//
// Uso:
//   k6 run tests/carga/extraccion_texto.js
//   k6 run --vus 20 --duration 1m -e PAGINAS=50 tests/carga/extraccion_texto.js
//
// Variables (-e):
//   BASE_URL  URL de la API           (default http://localhost:8000)
//   PAGINAS   páginas de cada PDF     (default 10)

import http from "k6/http";
import { check } from "k6";
import { Trend } from "k6/metrics";

const BASE_URL = __ENV.BASE_URL || "http://localhost:8000";
const PAGINAS = parseInt(__ENV.PAGINAS || "10", 10);
const LINEAS_POR_PAGINA = 60;
const PALABRAS = [
  "monolito", "servicio", "repositorio", "documento", "extraccion", "texto",
  "prueba", "carga", "latencia", "pagina", "arquitectura", "capa", "datos",
];

const tiempoExtraccion = new Trend("tiempo_extraccion_ms", true);

export const options = {
  vus: 5,
  duration: "30s",
  thresholds: {
    "http_req_failed{endpoint:subida}": ["rate<0.01"],
    // Límite amplio: está para que el resumen muestre la duración de la subida
    // sola (sin los DELETE) y poder compararla con tiempo_extraccion_ms.
    "http_req_duration{endpoint:subida}": ["p(95)<5000"],
    checks: ["rate>0.99"],
  },
};

function linea(marca, pagina, numero) {
  const palabras = [];
  for (let i = 0; i < 10; i++) {
    palabras.push(PALABRAS[(pagina * 7 + numero * 3 + i) % PALABRAS.length]);
  }
  return `${marca} p${pagina + 1} l${numero + 1} ${palabras.join(" ")}`;
}

// Arma un PDF 1.4 mínimo (solo ASCII: largo del string = bytes) con texto
// extraíble por pypdf. Objetos: 1 catálogo, 2 páginas, 3 fuente, y por cada
// página un objeto Page seguido de su stream de contenido.
function construirPdf(paginas, marca) {
  const objetos = [
    "<< /Type /Catalog /Pages 2 0 R >>",
    "",
    "<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica >>",
  ];
  const kids = [];
  for (let p = 0; p < paginas; p++) {
    const idPagina = objetos.length + 1;
    kids.push(`${idPagina} 0 R`);
    const lineas = [];
    for (let l = 0; l < LINEAS_POR_PAGINA; l++) {
      lineas.push(`(${linea(marca, p, l)}) Tj T*`);
    }
    const stream = `BT /F1 10 Tf 12 TL 40 800 Td ${lineas.join(" ")} ET`;
    objetos.push(
      `<< /Type /Page /Parent 2 0 R /MediaBox [0 0 595 842] ` +
        `/Resources << /Font << /F1 3 0 R >> >> /Contents ${idPagina + 1} 0 R >>`
    );
    objetos.push(`<< /Length ${stream.length} >>\nstream\n${stream}\nendstream`);
  }
  objetos[1] = `<< /Type /Pages /Kids [${kids.join(" ")}] /Count ${paginas} >>`;

  let pdf = "%PDF-1.4\n";
  const offsets = [];
  objetos.forEach((cuerpo, i) => {
    offsets.push(pdf.length);
    pdf += `${i + 1} 0 obj\n${cuerpo}\nendobj\n`;
  });
  const xref = pdf.length;
  pdf += `xref\n0 ${objetos.length + 1}\n0000000000 65535 f \n`;
  offsets.forEach((offset) => {
    pdf += `${String(offset).padStart(10, "0")} 00000 n \n`;
  });
  pdf += `trailer\n<< /Size ${objetos.length + 1} /Root 1 0 R >>\n`;
  pdf += `startxref\n${xref}\n%%EOF`;
  return pdf;
}

export default function () {
  const marca = `vu${__VU}-it${__ITER}-${Date.now()}`;
  const pdf = construirPdf(PAGINAS, marca);

  const respuesta = http.post(
    `${BASE_URL}/api/v1/pdfs/`,
    { file: http.file(pdf, `${marca}.pdf`, "application/pdf") },
    { tags: { endpoint: "subida" } }
  );

  const ok = check(respuesta, {
    "subida 201": (r) => r.status === 201,
    "trae X-Extraction-Time-Ms": (r) => r.headers["X-Extraction-Time-Ms"] !== undefined,
    "texto extraído": (r) => r.status === 201 && r.json("datos.contenido_pdf").includes(marca),
  });
  if (!ok) {
    return;
  }

  tiempoExtraccion.add(parseFloat(respuesta.headers["X-Extraction-Time-Ms"]));

  http.del(`${BASE_URL}/api/v1/pdfs/${respuesta.json("datos.id")}`, null, {
    tags: { endpoint: "borrado" },
  });
}
