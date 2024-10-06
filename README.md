# Batcher

|                |                                       |
| -------------- | ------------------------------------- |
| Name           | Batcher                           |
| Version        | v1.0.1                                |
| DockerHub | [beetaone/batcher](https://hub.docker.com/r/beetaone/batcher) |
| authors        | Jakub Grzelak                          |

- [Batcher](#batcher)
  - [Description](#description)
  - [Environment Variables](#environment-variables)
    - [Module Specific](#module-specific)
    - [Set by the beetaone Agent on the edge-node](#set-by-the-beetaone-agent-on-the-edge-node)
  - [Dependencies](#dependencies)
  - [Input](#input)
  - [Output](#output)

## Description

Batcher is responsible for collecting data into the batches and passing them later to the next module.
Batches could be defined by either a time frequency of data arrival or a file size.

## Environment Variables

### Module Specific

The following module configurations can be provided in a data service designer section on beetaone platform:

| Name                    | Environment Variables   | type   | Description                                              |
| ----------------------- | ----------------------- | ------ | -------------------------------------------------------- |
| File Size Batch Trigger | FILE_SIZE_BATCH_TRIGGER | float  | Size of a batch in kilobytes (kb)                        |
| Frequency Batch Trigger | FREQUENCY_BATCH_TRIGGER | float  | Length of time interval for collecting data into batches |
| Frequency Time Unit     | FREQUENCY_TIME_UNIT     | string | Unit of a time interval (ms - milliseconds, s - seconds, m - minutes, h - hours, d - days)  |


### Set by the beetaone Agent on the edge-node

Other features required for establishing the inter-container communication between modules in a data service are set by beetaone agent.

| Environment Variables | type   | Description                                    |
| --------------------- | ------ | ---------------------------------------------- |
| MODULE_NAME           | string | Name of the module                             |
| MODULE_TYPE           | string | Type of the module (Input, Processing, Output)  |
| EGRESS_URLS            | string | HTTP ReST endpoint for the next module         |
| INGRESS_HOST          | string | Host to which data will be received            |
| INGRESS_PORT          | string | Port to which data will be received            |

## Dependencies

```txt
bottle
requests
```

## Input

Input to this module is JSON body single object or array of objects:

Example of single object:

```json
{
  temperature: 15,
}
```

Example of array of objects:

```json
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

## Output

Output of this module is JSON body array of objects.

Example:

```json
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