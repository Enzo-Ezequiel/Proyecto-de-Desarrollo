"""
Validación rápida de Clean Code fixes sin dependencias externas.

Este script valida que todos los cambios de Clean Code fueron aplicados correctamente
sin necesidad de instalar todas las dependencias.
"""

import ast
import sys
from pathlib import Path

# Colores para output
GREEN = "\033[92m"
RED = "\033[91m"
YELLOW = "\033[93m"
RESET = "\033[0m"
BOLD = "\033[1m"


def check_file_exists(path: str) -> bool:
    """Verifica si un archivo existe."""
    return Path(path).exists()


def parse_python_file(path: str) -> ast.Module | None:
    """Parsea un archivo Python."""
    try:
        with open(path, "r", encoding="utf-8") as f:
            return ast.parse(f.read())
    except Exception as e:
        print(f"{RED}❌ Error parsing {path}: {e}{RESET}")
        return None


def find_function_or_method(tree: ast.Module, name: str) -> ast.AST | None:
    """Busca una función o método en el AST."""
    for node in ast.walk(tree):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            if node.name == name:
                return node
    return None


def find_class(tree: ast.Module, name: str) -> ast.ClassDef | None:
    """Busca una clase en el AST."""
    for node in ast.walk(tree):
        if isinstance(node, ast.ClassDef):
            if node.name == name:
                return node
    return None


def check_imports(tree: ast.Module, *module_names: str) -> bool:
    """Verifica si ciertos módulos están importados."""
    imports = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.ImportFrom):
            if node.module:
                imports.add(node.module)
        elif isinstance(node, ast.Import):
            for alias in node.names:
                imports.add(alias.name)
    return any(mod in imports for mod in module_names)


print(f"\n{BOLD}{'=' * 70}")
print(f"CLEAN CODE FIXES VALIDATION")
print(f"{'=' * 70}{RESET}\n")

checks_passed = 0
checks_failed = 0

# ============================================================================
# Check 1: Repository pattern file exists
# ============================================================================
print(f"{BOLD}1. Repository Pattern Implementation{RESET}")
if check_file_exists("/c/Programas/RepositorioDesarrollo/app/core/repository.py"):
    print(f"{GREEN}✅ repository.py file created{RESET}")
    repo_tree = parse_python_file(
        "/c/Programas/RepositorioDesarrollo/app/core/repository.py"
    )
    if repo_tree:
        if find_class(repo_tree, "Repository"):
            print(f"{GREEN}✅ Repository abstract class exists{RESET}")
            checks_passed += 1
        else:
            print(f"{RED}❌ Repository abstract class NOT found{RESET}")
            checks_failed += 1

        if find_class(repo_tree, "InMemoryRepository"):
            print(f"{GREEN}✅ InMemoryRepository implementation exists{RESET}")
            checks_passed += 1
        else:
            print(f"{RED}❌ InMemoryRepository NOT found{RESET}")
            checks_failed += 1
else:
    print(f"{RED}❌ repository.py file NOT created{RESET}")
    checks_failed += 2

# ============================================================================
# Check 2: User model type fixes
# ============================================================================
print(f"\n{BOLD}2. User Model Type Consistency{RESET}")
user_tree = parse_python_file("/c/Programas/RepositorioDesarrollo/app/models/user.py")
if user_tree:
    if check_imports(user_tree, "datetime"):
        print(f"{GREEN}✅ datetime imported in user.py{RESET}")
        checks_passed += 1
    else:
        print(f"{RED}❌ datetime NOT imported{RESET}")
        checks_failed += 1

    if check_imports(user_tree, "ValidationException", "app.core.exceptions"):
        print(f"{GREEN}✅ ValidationException imported{RESET}")
        checks_passed += 1
    else:
        print(f"{RED}❌ ValidationException NOT imported{RESET}")
        checks_failed += 1

# ============================================================================
# Check 3: Validation methods in User
# ============================================================================
print(f"\n{BOLD}3. Email Validation Consolidation{RESET}")
if user_tree:
    if find_function_or_method(user_tree, "_validate_email"):
        print(f"{GREEN}✅ _validate_email() method exists{RESET}")
        checks_passed += 1
    else:
        print(f"{RED}❌ _validate_email() method NOT found{RESET}")
        checks_failed += 1

    if find_function_or_method(user_tree, "_validate_full_name"):
        print(f"{GREEN}✅ _validate_full_name() method exists{RESET}")
        checks_passed += 1
    else:
        print(f"{RED}❌ _validate_full_name() method NOT found{RESET}")
        checks_failed += 1

# ============================================================================
# Check 4: BaseService Repository pattern
# ============================================================================
print(f"\n{BOLD}4. BaseService Repository Integration{RESET}")
base_service_tree = parse_python_file(
    "/c/Programas/RepositorioDesarrollo/app/services/base_service.py"
)
if base_service_tree:
    if check_imports(base_service_tree, "Repository", "InMemoryRepository"):
        print(f"{GREEN}✅ Repository imports in base_service.py{RESET}")
        checks_passed += 1
    else:
        print(f"{RED}❌ Repository imports NOT found{RESET}")
        checks_failed += 1

# ============================================================================
# Check 5: UserService consolidation
# ============================================================================
print(f"\n{BOLD}5. UserService Logic Consolidation{RESET}")
user_service_tree = parse_python_file(
    "/c/Programas/RepositorioDesarrollo/app/services/user_service.py"
)
if user_service_tree:
    if find_function_or_method(user_service_tree, "_apply_user_state_change"):
        print(f"{GREEN}✅ _apply_user_state_change() helper method exists{RESET}")
        checks_passed += 1
    else:
        print(f"{RED}❌ _apply_user_state_change() NOT found{RESET}")
        checks_failed += 1

    # Verify get_total_active_users is removed
    if not find_function_or_method(user_service_tree, "get_total_active_users"):
        print(f"{GREEN}✅ get_total_active_users() removed (YAGNI){RESET}")
        checks_passed += 1
    else:
        print(f"{YELLOW}⚠️  get_total_active_users() still exists{RESET}")

# ============================================================================
# Check 6: Controllers 404 helper
# ============================================================================
print(f"\n{BOLD}6. Controllers 404 Error Consolidation{RESET}")
controller_tree = parse_python_file(
    "/c/Programas/RepositorioDesarrollo/app/controllers/user_routes.py"
)
if controller_tree:
    if find_function_or_method(controller_tree, "_get_user_or_404"):
        print(f"{GREEN}✅ _get_user_or_404() helper exists{RESET}")
        checks_passed += 1
    else:
        print(f"{RED}❌ _get_user_or_404() NOT found{RESET}")
        checks_failed += 1

    if check_imports(controller_tree, "AppException"):
        print(f"{GREEN}✅ AppException imported in controllers{RESET}")
        checks_passed += 1
    else:
        print(f"{RED}❌ AppException NOT imported{RESET}")
        checks_failed += 1

# ============================================================================
# Check 7: Config constants
# ============================================================================
print(f"\n{BOLD}7. Configuration Constants{RESET}")
config_tree = parse_python_file("/c/Programas/RepositorioDesarrollo/app/core/config.py")
if config_tree:
    # Check if constants are defined
    has_constants = False
    with open("/c/Programas/RepositorioDesarrollo/app/core/config.py", "r") as f:
        content = f.read()
        if "APP_NAME" in content and "DEFAULT_HOST" in content:
            has_constants = True

    if has_constants:
        print(f"{GREEN}✅ Configuration constants defined{RESET}")
        checks_passed += 1
    else:
        print(f"{RED}❌ Configuration constants NOT found{RESET}")
        checks_failed += 1

# ============================================================================
# Check 8: Logging in utils
# ============================================================================
print(f"\n{BOLD}8. Logging Implementation{RESET}")
utils_tree = parse_python_file("/c/Programas/RepositorioDesarrollo/app/core/utils.py")
if utils_tree:
    if check_imports(utils_tree, "logging"):
        print(f"{GREEN}✅ logging module imported{RESET}")
        checks_passed += 1
    else:
        print(f"{RED}❌ logging module NOT imported{RESET}")
        checks_failed += 1

    # Check if validate_email function was removed
    if not find_function_or_method(utils_tree, "validate_email"):
        print(f"{GREEN}✅ validate_email() removed from utils (DRY){RESET}")
        checks_passed += 1
    else:
        print(f"{YELLOW}⚠️  validate_email() still exists in utils{RESET}")

# ============================================================================
# Check 9: Test fixtures
# ============================================================================
print(f"\n{BOLD}9. Test Fixtures Configuration{RESET}")
conftest_path = "/c/Programas/RepositorioDesarrollo/tests/conftest.py"
if check_file_exists(conftest_path):
    with open(conftest_path, "r") as f:
        conftest_content = f.read()

    if "TEST_VALID_EMAIL" in conftest_content:
        print(f"{GREEN}✅ Test constants defined in conftest{RESET}")
        checks_passed += 1
    else:
        print(f"{RED}❌ Test constants NOT found{RESET}")
        checks_failed += 1

    if "def user_service" in conftest_content:
        print(f"{GREEN}✅ user_service fixture created{RESET}")
        checks_passed += 1
    else:
        print(f"{RED}❌ user_service fixture NOT found{RESET}")
        checks_failed += 1

    if "def create_test_user" in conftest_content:
        print(f"{GREEN}✅ create_test_user factory function exists{RESET}")
        checks_passed += 1
    else:
        print(f"{RED}❌ create_test_user factory NOT found{RESET}")
        checks_failed += 1

# ============================================================================
# Check 10: DateTime fix
# ============================================================================
print(f"\n{BOLD}10. Deprecated datetime Fix{RESET}")
base_model_tree = parse_python_file(
    "/c/Programas/RepositorioDesarrollo/app/models/base_model.py"
)
if base_model_tree:
    if check_imports(base_model_tree, "timezone"):
        print(f"{GREEN}✅ timezone imported from datetime{RESET}")
        checks_passed += 1
    else:
        print(f"{RED}❌ timezone NOT imported{RESET}")
        checks_failed += 1

    with open("/c/Programas/RepositorioDesarrollo/app/models/base_model.py", "r") as f:
        base_model_content = f.read()
        if "datetime.now(timezone.utc)" in base_model_content:
            print(f"{GREEN}✅ datetime.now(timezone.utc) used{RESET}")
            checks_passed += 1
        else:
            print(f"{RED}❌ datetime.now(timezone.utc) NOT used{RESET}")
            checks_failed += 1

# ============================================================================
# Summary
# ============================================================================
print(f"\n{BOLD}{'=' * 70}")
print(f"VALIDATION SUMMARY")
print(f"{'=' * 70}{RESET}\n")

total_checks = checks_passed + checks_failed
percentage = (checks_passed / total_checks * 100) if total_checks > 0 else 0

print(f"{BOLD}Checks Passed:{RESET} {GREEN}{checks_passed}{RESET}")
print(f"{BOLD}Checks Failed:{RESET} {RED}{checks_failed}{RESET}")
print(f"{BOLD}Total Checks: {RESET}{total_checks}")
print(f"{BOLD}Success Rate: {RESET}{percentage:.1f}%\n")

if checks_failed == 0:
    print(f"{GREEN}{BOLD}✅ ALL CLEAN CODE FIXES VALIDATED SUCCESSFULLY!{RESET}\n")
    sys.exit(0)
else:
    print(f"{RED}{BOLD}❌ SOME CHECKS FAILED - SEE DETAILS ABOVE{RESET}\n")
    sys.exit(1)
