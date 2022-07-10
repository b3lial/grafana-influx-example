# grafana-example

Python script which adds an influxdb data source into grafana.
Afterwards, an example dashboard can be created with the following
query:

```
from(bucket: "cloudsensor")
  |> range(start: v.timeRangeStart, stop:v.timeRangeStop)
  |> filter(fn: (r) =>
    r._measurement == "office"
  )
```
