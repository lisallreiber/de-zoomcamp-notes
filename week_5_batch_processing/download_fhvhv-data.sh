# https://github.com/DataTalksClub/nyc-tlc-data/releases/download/fhvhv/fhvhv_tripdata_2021-06.csv.gz

URL_PREFIX="https://github.com/DataTalksClub/nyc-tlc-data/releases/download/fhvhv/"
YEAR=$1       # 2020, 2021
MONTH=$2      # 1-12

# format month
FMONTH=`printf "%02d" ${MONTH}`

# construct URL
URL="${URL_PREFIX}/fhvhv_tripdata_${YEAR}-${FMONTH}.csv.gz"
LOCAL_PREFIX="data/raw/fhvhv/${YEAR}/${FMONTH}"
LOCAL_FILE="fhvhv_tripdata_${YEAR}_${FMONTH}.csv.gz"
LOCAL_PATH="${LOCAL_PREFIX}/${LOCAL_FILE}"

echo "downloading ${URL} to ${LOCAL_PATH}"
mkdir -p ${LOCAL_PREFIX} 
wget ${URL} -O ${LOCAL_PATH}