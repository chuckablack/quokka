

export default function getStatusData(measurement, statusData) {

    let tsData = [];
    let maxY = 0;
    let yValue = 0;
    // const serviceData = this.state.serviceData.service_data;
    // console.log(statusData);

    for (let i = 0; i < statusData.length; i++) {

        if (measurement === "RSP_TIME") {
            yValue = (statusData[i].response_time)/1000;
        } else if (measurement === "AVAILABILITY") {
            yValue = statusData[i].availability ? 100 : 0;
        } else if (measurement === "AVAILABILITY_SUMMARY") {
            yValue = statusData[i].availability;
        }
        else {
            yValue = 0;
        }

        const tsDataItem = {x: new Date(statusData[i].timestamp), y: yValue};
        tsData.push(tsDataItem);
        if (tsDataItem.y > maxY) {
            maxY = tsDataItem.y;
        }
    }

    // console.log(tsData)
    return {tsData: tsData, maxY: maxY};
}