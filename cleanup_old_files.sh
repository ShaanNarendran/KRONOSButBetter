#!/bin/bash

# KRONOS Cleanup Script - Remove old/unused files after KRONOSv3 migration
echo "🧹 KRONOS Cleanup: Removing old files after KRONOSv3 migration..."

# Backup important files before deletion (just in case)
echo "📦 Creating backup of old files..."
mkdir -p .backup_old_kronos
cp -r backend .backup_old_kronos/ 2>/dev/null || true
cp simple_backend.py .backup_old_kronos/ 2>/dev/null || true
cp public/simulation_log.json .backup_old_kronos/ 2>/dev/null || true

# Remove old backend directory
if [ -d "backend" ]; then
    echo "🗑️  Removing old backend/ directory..."
    rm -rf backend/
fi

# Remove old simple backend file
if [ -f "simple_backend.py" ]; then
    echo "🗑️  Removing simple_backend.py..."
    rm -f simple_backend.py
fi

# Remove old static JSON file (now served by API)
if [ -f "public/simulation_log.json" ]; then
    echo "🗑️  Removing static simulation_log.json..."
    rm -f public/simulation_log.json
fi

# Remove old/redundant scripts
OLD_SCRIPTS=(
    "setup-dev.sh"
    "start.sh" 
    "run_all.sh"
    "quick-start.sh"
    "start_backend.sh"
    "start_frontend.sh"
)

for script in "${OLD_SCRIPTS[@]}"; do
    if [ -f "$script" ]; then
        echo "🗑️  Removing old script: $script"
        rm -f "$script"
    fi
done

# Keep only essential files
echo "✅ Cleanup complete! Kept files:"
echo "   📁 backend_v3/ - New KRONOSv3 backend"
echo "   📁 src/ - Updated frontend"  
echo "   📄 setup_backend_v3.sh - Backend setup"
echo "   📄 start_kronos.sh - App launcher"
echo "   📄 package.json - Frontend dependencies"

echo ""
echo "🔥 Old files backed up to .backup_old_kronos/"
echo "   (You can delete this folder once you confirm everything works)"

echo ""
echo "🚀 Your KRONOS app is now clean and ready!"
echo "   Run './run_kronos.sh' to start the application"