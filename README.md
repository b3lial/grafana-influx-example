# grafana-example

```
from(bucket: "cloudsensor")
  |> range(start: v.timeRangeStart, stop:v.timeRangeStop)
  |> filter(fn: (r) =>
    r._measurement == "office"
  )
```
