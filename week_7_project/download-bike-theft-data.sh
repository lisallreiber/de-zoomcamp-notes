# parameterized script to download the data each day
# and append it to the existing file

# get the date
TODAY=$1          # `date +%Y-%m-%d`
URL="https://www.internetwache-polizei-berlin.de/vdb/Fahrraddiebstahl.csv"

LOCAL_PREFIX="data/raw"
FILE_NAME="${TODAY}_berlin-bike-theft.csv"
LOCAL_PATH="${LOCAL_PREFIX}/${FILE_NAME}"

# download the data
echo "downloading ${URL} to ${LOCAL_PATH}"
# generate folder if it doesn't exist
mkdir -p ${LOCAL_PREFIX}
wget ${URL} -O ${LOCAL_PATH}

# echo the number of lines
# wc -l "${TODAY}_berlin-bike-theft.csv"
