DATE_START=$(date -d $(date +%Y)-01-01 +%Y-%m-%d) # Start date of the current year
DATE_END=$(date -d $(date -d +1year +%Y)-01-01 +%Y-%m-%d) # Start date of the next year
API_URL=https://mia.mobil.knute.edu.ua

SCRIPT_DIR=$(dirname $(realpath $0))
ROOT_DIR=$(dirname $SCRIPT_DIR)

echo $DATE_START $DATE_END

exit 0

# Check if cache is already loaded
if [ -f $ROOT_DIR/cache/temp-mkr-cache.loaded ]; then
    exit $(setup_cache)
fi

clear_temp_cache

# Install cacher if not installed
echo Installing cacher
bash $SCRIPT_DIR/install-cacher.sh -y || (
    echo Failed to install cacher
    exit 1
) && echo Cacher installed

# Load cache
bash $ROOT_DIR/tools/load_cache.sh -url=$API_URL -dateStart=$DATE_START -dateEnd=$DATE_END -output="$ROOT_DIR/cache/temp-mkr-cache.sqlite" || (
    echo Failed to load cache
    clear_temp_cache
    exit 1
)

setup_cache || exit 1


# Setup cache file
function setup_cache {
    mv $ROOT_DIR/cache/temp-mkr-cache.sqlite $ROOT_DIR/cache/mkr-cache.sqlite || (
        echo Failed to setup cache file. Perhaps you forgot to stop the bot first?
        touch $ROOT_DIR/cache/temp-mkr-cache.loaded
        return 1
    )
    clear_temp_cache
    echo Done
    return 0
}

# Function that clears broken cache in case of error
function clear_temp_cache {
    rm $ROOT_DIR/cache/temp-mkr-cache.* || (
        echo Failed to clear temp cache
        return 1
    )
    return 0
}
