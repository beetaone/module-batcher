# Batcher

|                |                                                                                   |
| -------------- | --------------------------------------------------------------------------------- |
| Name           | Batcher                                                                           |
| Version        | v0.0.2                                                                            |
| Dockerhub Link | [weevenetwork/weeve-batcher](https://hub.docker.com/r/weevenetwork/weeve-batcher) |
| authors        | Jakub Grzelak                                                                     |

- [Batcher](#batcher)
  - [Description](#description)
  - [Features](#features)
  - [Environment Variables](#environment-variables)
    - [Module Specific](#module-specific)
    - [Set by the weeve Agent on the edge-node](#set-by-the-weeve-agent-on-the-edge-node)
  - [Dependencies](#dependencies)
  - [Input](#input)
  - [Output](#output)
  - [Docker Compose Example](#docker-compose-example)

## Description

Batcher is responsible for collecting data into the batches and passing them later to the next module.
Batches could be defined by either a time frequency of data arrival or a file size.

## Features

- Collects data into batches
- Batches defined by time frequency or file size
- Flask ReST client
- Request - sends HTTP Request to the next module

## Environment Variables

### Module Specific

The following module configurations can be provided in a data service designer section on weeve platform:

| Name                    | Environment Variables   | type   | Description                                              |
| ----------------------- | ----------------------- | ------ | -------------------------------------------------------- |
| File Size Batch Trigger | FILE_SIZE_BATCH_TRIGGER | float  | Size of a batch in kilobytes (kb)                        |
| Frequency Batch Trigger | FREQUENCY_BATCH_TRIGGER | float  | Length of time interval for collecting data into batches |
| Frequency Time Unit     | FREQUENCY_TIME_UNIT     | string | Unit of a time interval (ms, s, m, h, d)                 |

Other features required for establishing the inter-container communication between modules in a data service are set by weeve agent.

### Set by the weeve Agent on the edge-node

| Environment Variables | type   | Description                            |
| --------------------- | ------ | -------------------------------------- |
| EGRESS_URL       | string | HTTP ReST endpoint for the next module |
| MODULE_NAME           | string | Name of the module                     |

## Dependencies

```txt
Flask==1.1.1
requests
python-dotenv
```

## Input

Input to this module is JSON body single object or array of objects:

Example of single object:

```node
{
  temperature: 15,
}
```

Example of array of objects:

```node
[
  {
    temperature: 13,
  },
  {
    temperature: 5,
  },
  {
    temperature: 7,
  },
];
```

## Output

Output of this module is JSON body array of objects.

Example:

```node
[
  {
    temperature: 54,
  },
  {
    temperature: 4,
  },
  {
    temperature: 66,
  },
];
```

## Docker Compose Example

```yml
version: "3"
services:
  batcher:
    image: weevenetwork/weeve-batcher
    environment:
      MODULE_NAME: weeve-batcher
      MODULE_TYPE: PROCESS
      EGRESS_URL: https://hookb.in/DrrdzwQwXgIdNNEwggLo
      FILE_SIZE_BATCH_TRIGGER: 1
      # FREQUENCY_BATCH_TRIGGER: 10
      FREQUENCY_TIME_UNIT: "s"
    ports:
      - 5000:80
```
