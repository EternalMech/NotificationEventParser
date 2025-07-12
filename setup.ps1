param(
    [string]$Command = "help"
)

function Show-Help {
    Write-Host "Notification Event Parser - Commands" -ForegroundColor Green
    Write-Host ""
    Write-Host "Available commands:" -ForegroundColor Yellow
    Write-Host "  full-setup    - Full build and start (recommended for first run)" -ForegroundColor Cyan
    Write-Host "  build         - Build all containers" -ForegroundColor Cyan
    Write-Host "  up            - Start all services" -ForegroundColor Cyan
    Write-Host "  down          - Stop all services" -ForegroundColor Cyan
    Write-Host "  restart       - Restart all services" -ForegroundColor Cyan
    Write-Host "  logs          - Show all service logs" -ForegroundColor Cyan
    Write-Host "  clean         - Clean all containers and volumes" -ForegroundColor Cyan
    Write-Host "  migrate       - Apply database migrations" -ForegroundColor Cyan
    Write-Host "  api           - Start only API server" -ForegroundColor Cyan
    Write-Host "  workers       - Start only workers" -ForegroundColor Cyan
    Write-Host "  help          - Show this help" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "Examples:" -ForegroundColor Yellow
    Write-Host "  .\setup.ps1 full-setup" -ForegroundColor White
    Write-Host "  .\setup.ps1 logs" -ForegroundColor White
}

function Full-Setup {
    Write-Host "Starting full project build..." -ForegroundColor Green
    
    Write-Host "Stopping and cleaning containers..." -ForegroundColor Yellow
    docker-compose down -v --remove-orphans
    
    Write-Host "Building containers..." -ForegroundColor Yellow
    docker-compose build
    
    Write-Host "Starting PostgreSQL..." -ForegroundColor Yellow
    docker-compose up postgres -d
    Start-Sleep -Seconds 10
    
    Write-Host "Applying migrations..." -ForegroundColor Yellow
    docker-compose up alembic -d
    Start-Sleep -Seconds 5
    
    Write-Host "Starting all services..." -ForegroundColor Yellow
    docker-compose up -d
    
    Write-Host ""
    Write-Host "Project successfully started!" -ForegroundColor Green
    Write-Host "API available at: http://localhost:8000" -ForegroundColor Cyan
    Write-Host "API documentation: http://localhost:8000/docs" -ForegroundColor Cyan
    Write-Host "For logs run: .\setup.ps1 logs" -ForegroundColor Cyan
}

switch ($Command.ToLower()) {
    "full-setup" { Full-Setup }
    "build" { docker-compose build }
    "up" { docker-compose up -d }
    "down" { docker-compose down }
    "restart" { docker-compose restart }
    "logs" { docker-compose logs -f }
    "clean" { 
        docker-compose down -v --remove-orphans
        docker system prune -f
    }
    "migrate" { 
        docker-compose up alembic -d
        Start-Sleep -Seconds 5
        docker-compose logs alembic
    }
    "api" { docker-compose up api -d }
    "workers" { docker-compose up kudago_worker notification_worker -d }
    default { Show-Help }
} 