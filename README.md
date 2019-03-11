# nfn-faas
## Functions as a Service for Notes from Nature

This repo contains the Field Book functions for NfN as well as the [OpenFaaS](https://github.com/openfaas/faas)-built makings of a Docker container. The built container is located on [Dockerhub](https://hub.docker.com/r/zooniverse/nfn_fieldbook/). This container lives in Docker Swarm. It's designed to be used as an external extractor for [Caesar](https://github.com/zooniverse/caesar). 

The `nfn_fieldbook` function takes a Caesar-style Classification as its input and returns returns a JSON object of the badges that are relevant to this classification. An example request would look like this:

`POST /function/nfn_fieldbook?year=T10&country=T1&state=T2&workflow=herbarium`

Note the mappings of "badge" and workflow task in the query params. Your POST body should just be a Caesar-formatted classification.

Currently implemented badges:

### Time
The classification's `created_at` value is examined for the purpose of awarding time-specific badges:

| Response Value | Time |
| --------------- | ---- |
| `nightowl` | 2100 < .created_at < 0300 |
| `earlybird` | 0300 < .created_at < 0900 |
| `lunchbreak` | 0900 < .created_at < 1500 |
| `dinnertime` | 1500 < .created_at < 2100 |

This uses the `utc_offset` value in the classification metadata in order to correctly calculate the time at the location the user made the classification.

### Decade
Searches for the year in either a) the subject metadata or b) the annotation, indicated by the task number in the query param, in that order. 

So if 'year' (downcased) is found as a key in the subject metadata, with a value of "1999", `{'decade': '90s'}` will be returned. 

If the metadata doesn't have a year but the query params contain `?year=T10`, then that task's value will be returned:

```
{
  "task": "T10",
  "value": [
    {
      "value": 1983,
      "option": true
    }
  ]
}
```

will include `{'decade': '80s'}` in the response. These values will be stats-reduced.

### Country and State
The annotation is flattened and searched for the task key indicated and the value returned.

```
{
  "task": "T1",
  "value": [
    {
      "value": "United States",
      "option": true
    }
  ]
}
```

will return `{'country': 'United States'}` in the response.


### Earth Day
`{ "earth_day": true }` is included with the classification's `created_at` date was on April 22.

### Workflow
Currently, the workflow included in the query param (i.e. `?workflow=herbarium`) is returned in the response unchanged for later reduction.
