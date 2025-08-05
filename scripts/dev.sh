#!/bin/bash

# AI Coder Agent Development Script
# This script provides common development tasks for the AI Coder Agent project

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Project configuration
PROJECT_NAME="AI Coder Agent"
PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
BACKEND_DIR="$PROJECT_ROOT/backend"
FRONTEND_DIR="$PROJECT_ROOT/frontend"

# Logging functions
log_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

log_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

log_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Check prerequisites
check_prerequisites() {
    log_info "Checking prerequisites..."
    
    local missing_deps=()
    
    if ! command_exists python3; then
        missing_deps+=("python3")
    fi
    
    if ! command_exists node; then
        missing_deps+=("node")
    fi
    
    if ! command_exists docker; then
        missing_deps+=("docker")
    fi
    
    if ! command_exists docker-compose; then
        missing_deps+=("docker-compose")
    fi
    
    if [ ${#missing_deps[@]} -ne 0 ]; then
        log_error "Missing dependencies: ${missing_deps[*]}"
        log_info "Please install the missing dependencies and try again."
        exit 1
    fi
    
    log_success "All prerequisites are installed"
}

# Setup environment
setup_env() {
    log_info "Setting up environment..."
    
    if [ ! -f "$PROJECT_ROOT/.env" ]; then
        cp "$PROJECT_ROOT/.env.example" "$PROJECT_ROOT/.env"
        log_success "Created .env file from .env.example"
        log_warning "Please update .env with your actual configuration"
    else
        log_info ".env file already exists"
    fi
}

# Setup backend
setup_backend() {
    log_info "Setting up backend..."
    
    if [ ! -d "$BACKEND_DIR" ]; then
        log_error "Backend directory not found"
        exit 1
    fi
    
    cd "$BACKEND_DIR"
    
    # Create virtual environment if it doesn't exist
    if [ ! -d "venv" ]; then
        log_info "Creating Python virtual environment..."
        python3 -m venv venv
    fi
    
    # Activate virtual environment
    source venv/bin/activate
    
    # Install dependencies
    if [ -f "requirements.txt" ]; then
        log_info "Installing Python dependencies..."
        pip install -r requirements.txt
    fi
    
    if [ -f "requirements-dev.txt" ]; then
        log_info "Installing development dependencies..."
        pip install -r requirements-dev.txt
    fi
    
    log_success "Backend setup complete"
}

# Setup frontend
setup_frontend() {
    log_info "Setting up frontend..."
    
    if [ ! -d "$FRONTEND_DIR" ]; then
        log_error "Frontend directory not found"
        exit 1
    fi
    
    cd "$FRONTEND_DIR"
    
    # Install dependencies
    if [ -f "package.json" ]; then
        log_info "Installing Node.js dependencies..."
        npm install
    fi
    
    log_success "Frontend setup complete"
}

# Start development servers
start_dev() {
    log_info "Starting development servers..."
    
    # Start database
    log_info "Starting PostgreSQL database..."
    docker-compose up -d postgres redis
    
    # Wait for database to be ready
    log_info "Waiting for database to be ready..."
    sleep 10
    
    # Start backend
    log_info "Starting backend server..."
    cd "$BACKEND_DIR"
    source venv/bin/activate
    uvicorn autodev_agent.main:app --reload --host 0.0.0.0 --port 8000 &
    BACKEND_PID=$!
    
    # Start frontend
    log_info "Starting frontend server..."
    cd "$FRONTEND_DIR"
    npm run dev &
    FRONTEND_PID=$!
    
    log_success "Development servers started"
    log_info "Backend: http://localhost:8000"
    log_info "Frontend: http://localhost:5173"
    log_info "Press Ctrl+C to stop all servers"
    
    # Wait for interrupt
    trap "kill $BACKEND_PID $FRONTEND_PID; exit" INT
    wait
}

# Run tests
run_tests() {
    log_info "Running tests..."
    
    # Backend tests
    if [ -d "$BACKEND_DIR" ]; then
        log_info "Running backend tests..."
        cd "$BACKEND_DIR"
        source venv/bin/activate
        pytest --cov=autodev_agent --cov-report=html
    fi
    
    # Frontend tests
    if [ -d "$FRONTEND_DIR" ]; then
        log_info "Running frontend tests..."
        cd "$FRONTEND_DIR"
        npm test
    fi
    
    log_success "Tests completed"
}

# Run linting
run_lint() {
    log_info "Running linting..."
    
    # Backend linting
    if [ -d "$BACKEND_DIR" ]; then
        log_info "Running backend linting..."
        cd "$BACKEND_DIR"
        source venv/bin/activate
        
        if command_exists ruff; then
            ruff check .
        fi
        
        if command_exists black; then
            black --check .
        fi
        
        if command_exists mypy; then
            mypy .
        fi
    fi
    
    # Frontend linting
    if [ -d "$FRONTEND_DIR" ]; then
        log_info "Running frontend linting..."
        cd "$FRONTEND_DIR"
        npm run lint
    fi
    
    log_success "Linting completed"
}

# Format code
format_code() {
    log_info "Formatting code..."
    
    # Backend formatting
    if [ -d "$BACKEND_DIR" ]; then
        log_info "Formatting backend code..."
        cd "$BACKEND_DIR"
        source venv/bin/activate
        
        if command_exists black; then
            black .
        fi
        
        if command_exists isort; then
            isort .
        fi
    fi
    
    # Frontend formatting
    if [ -d "$FRONTEND_DIR" ]; then
        log_info "Formatting frontend code..."
        cd "$FRONTEND_DIR"
        npm run format
    fi
    
    log_success "Code formatting completed"
}

# Build project
build_project() {
    log_info "Building project..."
    
    # Build backend
    if [ -d "$BACKEND_DIR" ]; then
        log_info "Building backend..."
        cd "$BACKEND_DIR"
        source venv/bin/activate
        python setup.py build
    fi
    
    # Build frontend
    if [ -d "$FRONTEND_DIR" ]; then
        log_info "Building frontend..."
        cd "$FRONTEND_DIR"
        npm run build
    fi
    
    log_success "Project build completed"
}

# Clean project
clean_project() {
    log_info "Cleaning project..."
    
    # Clean Python cache
    find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
    find . -type f -name "*.pyc" -delete 2>/dev/null || true
    
    # Clean Node.js cache
    if [ -d "$FRONTEND_DIR" ]; then
        cd "$FRONTEND_DIR"
        rm -rf node_modules/.cache 2>/dev/null || true
    fi
    
    # Clean build artifacts
    rm -rf build/ dist/ *.egg-info/ 2>/dev/null || true
    
    log_success "Project cleaned"
}

# Show help
show_help() {
    echo "Usage: $0 [COMMAND]"
    echo ""
    echo "Commands:"
    echo "  setup       Setup the development environment"
    echo "  start       Start development servers"
    echo "  test        Run tests"
    echo "  lint        Run linting"
    echo "  format      Format code"
    echo "  build       Build project"
    echo "  clean       Clean project"
    echo "  help        Show this help message"
    echo ""
    echo "Examples:"
    echo "  $0 setup    # Setup development environment"
    echo "  $0 start    # Start development servers"
    echo "  $0 test     # Run all tests"
}

# Main script
main() {
    case "${1:-help}" in
        setup)
            check_prerequisites
            setup_env
            setup_backend
            setup_frontend
            log_success "Development environment setup complete"
            ;;
        start)
            start_dev
            ;;
        test)
            run_tests
            ;;
        lint)
            run_lint
            ;;
        format)
            format_code
            ;;
        build)
            build_project
            ;;
        clean)
            clean_project
            ;;
        help|--help|-h)
            show_help
            ;;
        *)
            log_error "Unknown command: $1"
            show_help
            exit 1
            ;;
    esac
}

# Run main function
main "$@"