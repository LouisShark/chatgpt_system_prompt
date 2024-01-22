GPT URL: https://chat.openai.com/g/g-6fHDdLMRC-national-park-explorer

GPT Title: National Park Explorer

GPT Description: Plan a trip and explore America the Beautiful - By Merrick D Christensen

GPT instructions:

```markdown
You are an excellent trip planner who knows everything about National Parks. You provide plans with suggestions of things to do and you always show images and media to make the plans exciting. When someone is planning a trip, use the things to do action to provide extra details for specific things to do for that specific park. You won't have enough information without looking up things to do.

Use the actions provided to answer questions. If the response includes an image display it in the response. For example, if you're listing out parks, include an image for that park. If your sharing assets from a galley that contain an image, include the image in your response. When you reply include suggestions for their response. For example, if they ask about a specific park? Ask them if they'd like to see galleries related to the park, see things to do or plan a trip to that park. 

When giving a response try and use the galleries actions to include images. For example, if you're replying about a specific Trail or activity and you don't have an image you can retrieve an image of the trail from the gallery action. Even if the user isn't asking for an image, try and retrieve a relevant image and include it in your response.

Even if the user doesn't mention National Parks, assume that they are referring to that. Your actions support a q and sort parameter that can be used to further filter your searches.

Be sure to include images throughout the itinerary response when planning a trip. When you are giving things to do, provide the necessary information for knowing if it is a good option, for example its fees and permits.
```

GPT Actions:

```json
{
  "openapi": "3.1.0",
  "info": {
    "version": "1.0.0",
    "title": "OpenAPI"
  },
  "servers": [ { "url": "https://nps-gpt.merrick-christensen.workers.dev" } ],
  "components": {
    "schemas": {
      "Activity": {
        "type": "object",
        "properties": {
          "id": {
            "type": "string"
          },
          "name": {
            "type": "string"
          }
        },
        "required": [
          "id",
          "name"
        ]
      },
      "Phone Number": {
        "type": "object",
        "properties": {
          "phoneNumber": {
            "type": "string"
          },
          "description": {
            "type": "string"
          },
          "extension": {
            "type": "string"
          },
          "type": {
            "type": "string",
            "enum": [
              "Voice",
              "Fax",
              "TTY"
            ]
          }
        },
        "required": [
          "phoneNumber",
          "description",
          "extension",
          "type"
        ]
      },
      "Email Address": {
        "type": "object",
        "properties": {
          "emailAddress": {
            "type": "string"
          },
          "description": {
            "type": "string"
          }
        },
        "required": [
          "emailAddress",
          "description"
        ]
      },
      "Entrance Fee": {
        "type": "object",
        "properties": {
          "cost": {
            "type": "string"
          },
          "description": {
            "type": "string"
          },
          "title": {
            "type": "string"
          }
        },
        "required": [
          "cost",
          "description",
          "title"
        ]
      },
      "Entrance Pass": {
        "type": "object",
        "properties": {
          "cost": {
            "type": "string"
          },
          "description": {
            "type": "string"
          },
          "title": {
            "type": "string"
          }
        },
        "required": [
          "cost",
          "description",
          "title"
        ]
      },
      "Image": {
        "type": "object",
        "properties": {
          "credit": {
            "type": "string",
            "description": "Credit for the image"
          },
          "altText": {
            "type": "string"
          },
          "title": {
            "type": "string"
          },
          "caption": {
            "type": "string"
          },
          "url": {
            "type": "string"
          }
        },
        "required": [
          "credit",
          "altText",
          "title",
          "caption",
          "url"
        ]
      },
      "Hours": {
        "type": "object",
        "properties": {
          "sunday": {
            "type": "string"
          },
          "monday": {
            "type": "string"
          },
          "tuesday": {
            "type": "string"
          },
          "wednesday": {
            "type": "string"
          },
          "thursday": {
            "type": "string"
          },
          "friday": {
            "type": "string"
          },
          "saturday": {
            "type": "string"
          }
        },
        "required": [
          "sunday",
          "monday",
          "tuesday",
          "wednesday",
          "thursday",
          "friday",
          "saturday"
        ]
      },
      "Operating Hours": {
        "type": "object",
        "properties": {
          "name": {
            "type": "string"
          },
          "description": {
            "type": "string"
          },
          "standardHours": {
            "$ref": "#/components/schemas/Hours"
          },
          "exceptions": {
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "name": {
                  "type": "string"
                },
                "startDate": {
                  "type": "string"
                },
                "endDate": {
                  "type": "string"
                },
                "exceptionHours": {
                  "$ref": "#/components/schemas/Hours"
                }
              },
              "required": [
                "name",
                "startDate",
                "endDate",
                "exceptionHours"
              ]
            }
          }
        },
        "required": [
          "name",
          "description",
          "standardHours",
          "exceptions"
        ]
      },
      "Topic": {
        "type": "object",
        "properties": {
          "id": {
            "type": "string"
          },
          "name": {
            "type": "string"
          }
        },
        "required": [
          "id",
          "name"
        ]
      },
      "Park": {
        "type": "object",
        "properties": {
          "id": {
            "type": "string"
          },
          "name": {
            "type": "string"
          },
          "weatherInfo": {
            "type": "string"
          },
          "activities": {
            "type": "array",
            "items": {
              "$ref": "#/components/schemas/Activity"
            }
          },
          "contacts": {
            "type": "object",
            "properties": {
              "phoneNumbers": {
                "type": "array",
                "items": {
                  "$ref": "#/components/schemas/Phone Number"
                }
              },
              "emailAddresses": {
                "type": "array",
                "items": {
                  "$ref": "#/components/schemas/Email Address"
                }
              }
            },
            "required": [
              "phoneNumbers",
              "emailAddresses"
            ]
          },
          "description": {
            "type": "string",
            "description": "Introductory paragraph from the park homepage\t"
          },
          "designation": {
            "type": "string",
            "description": "national park"
          },
          "directionsInfo": {
            "type": "string"
          },
          "directionsUrl": {
            "type": "string"
          },
          "entranceFees": {
            "type": "array",
            "items": {
              "$ref": "#/components/schemas/Entrance Fee"
            }
          },
          "entrancePasses": {
            "type": "array",
            "items": {
              "$ref": "#/components/schemas/Entrance Pass"
            }
          },
          "fullName": {
            "type": "string"
          },
          "images": {
            "type": "array",
            "items": {
              "$ref": "#/components/schemas/Image"
            }
          },
          "latLong": {
            "type": "string"
          },
          "latitude": {
            "type": "string"
          },
          "longitude": {
            "type": "string"
          },
          "operatingHours": {
            "type": "array",
            "items": {
              "$ref": "#/components/schemas/Operating Hours"
            }
          },
          "parkCode": {
            "type": "string"
          },
          "relevanceScore": {
            "type": "number"
          },
          "states": {
            "type": "string"
          },
          "topics": {
            "type": "array",
            "items": {
              "$ref": "#/components/schemas/Topic"
            }
          },
          "url": {
            "type": "string"
          }
        },
        "required": [
          "id",
          "name",
          "weatherInfo",
          "activities",
          "contacts",
          "description",
          "designation",
          "directionsInfo",
          "directionsUrl",
          "entranceFees",
          "entrancePasses",
          "fullName",
          "images",
          "latLong",
          "latitude",
          "longitude",
          "operatingHours",
          "parkCode",
          "relevanceScore",
          "states",
          "topics",
          "url"
        ]
      },
      "Gallery Image": {
        "type": "object",
        "properties": {
          "altText": {
            "type": "string"
          },
          "title": {
            "type": "string"
          },
          "description": {
            "type": "string"
          },
          "url": {
            "type": "string"
          }
        },
        "required": [
          "altText",
          "title",
          "description",
          "url"
        ]
      },
      "Related Park": {
        "type": "object",
        "properties": {
          "states": {
            "type": "string"
          },
          "parkCode": {
            "type": "string"
          },
          "designation": {
            "type": "string"
          },
          "fullName": {
            "type": "string"
          },
          "url": {
            "type": "string"
          },
          "name": {
            "type": "string"
          }
        },
        "required": [
          "states",
          "parkCode",
          "designation",
          "fullName",
          "url",
          "name"
        ]
      },
      "Gallery": {
        "type": "object",
        "properties": {
          "id": {
            "type": "string"
          },
          "url": {
            "type": "string"
          },
          "title": {
            "type": "string"
          },
          "description": {
            "type": "string"
          },
          "images": {
            "type": "array",
            "items": {
              "$ref": "#/components/schemas/Gallery Image"
            }
          },
          "relatedParks": {
            "type": "array",
            "items": {
              "$ref": "#/components/schemas/Related Park"
            }
          },
          "tags": {
            "type": "array",
            "items": {
              "type": "string"
            }
          },
          "credit": {
            "type": "string"
          },
          "constraintsInfo": {
            "type": "object",
            "properties": {
              "constraint": {
                "type": "string"
              },
              "grantingRights": {
                "type": "string"
              }
            },
            "required": [
              "constraint",
              "grantingRights"
            ]
          },
          "copyright": {
            "type": "string"
          }
        },
        "required": [
          "id",
          "url",
          "title",
          "description",
          "images",
          "relatedParks",
          "tags",
          "credit",
          "constraintsInfo",
          "copyright"
        ]
      },
      "Gallery Asset": {
        "type": "object",
        "properties": {
          "id": {
            "type": "string"
          },
          "permalinkUrl": {
            "type": "string"
          },
          "title": {
            "type": "string"
          },
          "description": {
            "type": "string"
          },
          "altText": {
            "type": "string"
          },
          "fileInfo": {
            "type": "object",
            "properties": {
              "url": {
                "type": "string"
              },
              "fileType": {
                "type": "string"
              },
              "widthPixels": {
                "type": "string"
              },
              "heightPixels": {
                "type": "string"
              },
              "fileSizeKb": {
                "type": "string"
              }
            },
            "required": [
              "url",
              "fileType",
              "widthPixels",
              "heightPixels",
              "fileSizeKb"
            ]
          },
          "relatedParks": {
            "type": "array",
            "items": {
              "$ref": "#/components/schemas/Related Park"
            }
          },
          "tags": {
            "type": "array",
            "items": {
              "type": "string"
            }
          },
          "credit": {
            "type": "string"
          },
          "constraintsInfo": {
            "type": "object",
            "properties": {
              "constraint": {
                "type": "string"
              },
              "grantingRights": {
                "type": "string"
              }
            },
            "required": [
              "constraint",
              "grantingRights"
            ]
          },
          "copyright": {
            "type": "string"
          },
          "ordinal": {
            "type": "string"
          }
        },
        "required": [
          "id",
          "permalinkUrl",
          "title",
          "description",
          "altText",
          "fileInfo",
          "relatedParks",
          "tags",
          "credit",
          "constraintsInfo",
          "copyright",
          "ordinal"
        ]
      }
    },
    "parameters": {}
  },
  "paths": {
    "/api/parks": {
      "get": {
        "tags": [
          "Parks"
        ],
        "summary": "List Parks",
        "operationId": "get_ParkList",
        "parameters": [
          {
            "schema": {
              "type": "array",
              "items": {
                "type": "string"
              },
              "description": "A comma delimited list of park codes (each 4-10 characters in length)."
            },
            "required": false,
            "name": "parkCode",
            "in": "query"
          },
          {
            "schema": {
              "type": "array",
              "items": {
                "type": "string"
              },
              "description": "A comma delimited list of 2 character state codes.",
              "example": "CA,UT"
            },
            "required": false,
            "name": "stateCode",
            "in": "query"
          },
          {
            "schema": {
              "type": "array",
              "items": {
                "type": "string"
              },
              "description": "A list of resource properties to sort the results by. Ascending order is assumed for each property. If descending order is desired, the unary negative should prefix the property name. Invalid property values will be ignored. If no sort parameter is passed in a request, the default sort is by fullName. If sorting by relevanceScore, you 1) will likely use -relevanceScore as a higher score indicates a more relevant result and 2) cannot use it in conjunction with other sort properties. Possible fields to sort by are fullName, parkCode, and relevanceScore."
            },
            "required": false,
            "name": "sort",
            "in": "query"
          },
          {
            "schema": {
              "type": "string",
              "default": "5",
              "description": "Number of results to return per request. Default is 5.",
              "example": "5"
            },
            "required": false,
            "name": "limit",
            "in": "query"
          },
          {
            "schema": {
              "type": "string",
              "description": "Get the next [limit] results starting with this number. Default is 0."
            },
            "required": false,
            "name": "start",
            "in": "query"
          },
          {
            "schema": {
              "type": "string",
              "description": "Term to search on"
            },
            "required": false,
            "name": "q",
            "in": "query"
          }
        ],
        "responses": {
          "200": {
            "description": "Returns a list of parks",
            "content": {
              "application/json": {
                "schema": {
                  "type": "object",
                  "properties": {
                    "total": {
                      "type": "string",
                      "description": "Total number of results"
                    },
                    "limit": {
                      "type": "string",
                      "description": "Number of results per request"
                    },
                    "start": {
                      "type": "string",
                      "description": "Start position of results"
                    },
                    "data": {
                      "type": "array",
                      "items": {
                        "$ref": "#/components/schemas/Park"
                      }
                    }
                  },
                  "required": [
                    "total",
                    "limit",
                    "start",
                    "data"
                  ]
                }
              }
            }
          }
        }
      }
    },
    "/api/activities": {
      "get": {
        "tags": [
          "Activities"
        ],
        "summary": "List Activities",
        "operationId": "get_ActivityList",
        "parameters": [
          {
            "schema": {
              "type": "array",
              "items": {
                "type": "string"
              },
              "description": "A comma delimited list of fields to sort the results by. Ascending order is assumed for each field unless the field name is prefixed with the unary negative which implies descending order."
            },
            "required": false,
            "name": "sort",
            "in": "query"
          },
          {
            "schema": {
              "type": "string",
              "default": "5",
              "description": "Number of results to return per request. Default is 5.",
              "example": "5"
            },
            "required": false,
            "name": "limit",
            "in": "query"
          },
          {
            "schema": {
              "type": "string",
              "description": "Get the next [limit] results starting with this number. Default is 0."
            },
            "required": false,
            "name": "start",
            "in": "query"
          },
          {
            "schema": {
              "type": "string",
              "description": "Term to search on"
            },
            "required": false,
            "name": "q",
            "in": "query"
          }
        ],
        "responses": {
          "200": {
            "description": "Retrieve categories of activities (astronomy, hiking, wildlife watching, etc.) possible in national parks.",
            "content": {
              "application/json": {
                "schema": {
                  "type": "object",
                  "properties": {
                    "total": {
                      "type": "string",
                      "description": "Total number of results"
                    },
                    "limit": {
                      "type": "string",
                      "description": "Number of results per request"
                    },
                    "start": {
                      "type": "string",
                      "description": "Start position of results"
                    },
                    "data": {
                      "type": "array",
                      "items": {
                        "$ref": "#/components/schemas/Activity"
                      }
                    }
                  },
                  "required": [
                    "total",
                    "limit",
                    "start",
                    "data"
                  ]
                }
              }
            }
          }
        }
      }
    },
    "/api/activities/parks": {
      "get": {
        "tags": [
          "Parks"
        ],
        "summary": "Retrieve national parks that are related to particular categories of activity (astronomy, hiking, wildlife watching, etc.).",
        "operationId": "get_ParkListByActivity",
        "parameters": [
          {
            "schema": {
              "type": "array",
              "items": {
                "type": "string"
              },
              "description": "A comma delimited list of activity IDs."
            },
            "required": false,
            "name": "id",
            "in": "query"
          },
          {
            "schema": {
              "type": "array",
              "items": {
                "type": "string"
              },
              "description": "A comma delimited list of fields to sort the results by. Ascending order is assumed for each field unless the field name is prefixed with the unary negative which implies descending order."
            },
            "required": false,
            "name": "sort",
            "in": "query"
          },
          {
            "schema": {
              "type": "string",
              "default": "5",
              "description": "Number of results to return per request. Default is 5.",
              "example": "5"
            },
            "required": false,
            "name": "limit",
            "in": "query"
          },
          {
            "schema": {
              "type": "string",
              "description": "Get the next [limit] results starting with this number. Default is 0."
            },
            "required": false,
            "name": "start",
            "in": "query"
          },
          {
            "schema": {
              "type": "string",
              "description": "Term to search on"
            },
            "required": false,
            "name": "q",
            "in": "query"
          }
        ],
        "responses": {
          "200": {
            "description": "Returns a list of parks",
            "content": {
              "application/json": {
                "schema": {
                  "type": "object",
                  "properties": {
                    "total": {
                      "type": "string",
                      "description": "Total number of results"
                    },
                    "limit": {
                      "type": "string",
                      "description": "Number of results per request"
                    },
                    "start": {
                      "type": "string",
                      "description": "Start position of results"
                    },
                    "data": {
                      "type": "object",
                      "properties": {
                        "id": {
                          "type": "string",
                          "description": "Unique identifier for activity park."
                        },
                        "name": {
                          "type": "string",
                          "description": "Name for activity park."
                        },
                        "parks": {
                          "type": "array",
                          "items": {
                            "type": "object",
                            "properties": {
                              "states": {
                                "type": "string",
                                "description": "Comma delimited list of two letter state codes"
                              },
                              "fullName": {
                                "type": "string",
                                "description": "Full name of the park"
                              },
                              "url": {
                                "type": "string",
                                "description": "URL of the park's website"
                              },
                              "parkCode": {
                                "type": "string",
                                "description": "Unique 4 character code for the park"
                              },
                              "designation": {
                                "type": "string",
                                "description": "The parks official designation"
                              },
                              "name": {
                                "type": "string",
                                "description": "Name of the park"
                              }
                            },
                            "required": [
                              "states",
                              "fullName",
                              "url",
                              "parkCode",
                              "designation",
                              "name"
                            ]
                          }
                        }
                      },
                      "required": [
                        "id",
                        "name",
                        "parks"
                      ]
                    }
                  },
                  "required": [
                    "total",
                    "limit",
                    "start",
                    "data"
                  ]
                }
              }
            }
          }
        }
      }
    },
    "/api/multimedia/galleries": {
      "get": {
        "tags": [
          "Parks"
        ],
        "summary": "List Parks",
        "operationId": "get_GalleriesList",
        "parameters": [
          {
            "schema": {
              "type": "array",
              "items": {
                "type": "string"
              },
              "description": "A comma delimited list of park codes (each 4-10 characters in length)."
            },
            "required": false,
            "name": "parkCode",
            "in": "query"
          },
          {
            "schema": {
              "type": "array",
              "items": {
                "type": "string"
              },
              "description": "A comma delimited list of 2 character state codes.",
              "example": "CA,UT"
            },
            "required": false,
            "name": "stateCode",
            "in": "query"
          },
          {
            "schema": {
              "type": "string",
              "default": "5",
              "description": "Number of results to return per request. Default is 5.",
              "example": "5"
            },
            "required": false,
            "name": "limit",
            "in": "query"
          },
          {
            "schema": {
              "type": "string",
              "description": "Get the next [limit] results starting with this number. Default is 0."
            },
            "required": false,
            "name": "start",
            "in": "query"
          },
          {
            "schema": {
              "type": "string",
              "description": "Term to search on"
            },
            "required": false,
            "name": "q",
            "in": "query"
          }
        ],
        "responses": {
          "200": {
            "description": "Returns galleries created by national parks and other NPS entities.",
            "content": {
              "application/json": {
                "schema": {
                  "type": "object",
                  "properties": {
                    "total": {
                      "type": "string",
                      "description": "Total number of results"
                    },
                    "limit": {
                      "type": "string",
                      "description": "Number of results per request"
                    },
                    "start": {
                      "type": "string",
                      "description": "Start position of results"
                    },
                    "data": {
                      "type": "array",
                      "items": {
                        "$ref": "#/components/schemas/Gallery"
                      }
                    }
                  },
                  "required": [
                    "total",
                    "limit",
                    "start",
                    "data"
                  ]
                }
              }
            }
          }
        }
      }
    },
    "/api/multimedia/galleries/assets": {
      "get": {
        "tags": [
          "Gallery"
        ],
        "summary": "List gallery assets by unique asset id, or gallery id, etc",
        "operationId": "get_GalleryAssetsList",
        "parameters": [
          {
            "schema": {
              "type": "array",
              "items": {
                "type": "string"
              },
              "description": "A comma delimited list of park codes (each 4-10 characters in length)."
            },
            "required": false,
            "name": "parkCode",
            "in": "query"
          },
          {
            "schema": {
              "type": "array",
              "items": {
                "type": "string"
              },
              "description": "A comma delimited list of 2 character state codes.",
              "example": "CA,UT"
            },
            "required": false,
            "name": "stateCode",
            "in": "query"
          },
          {
            "schema": {
              "type": "string",
              "default": "5",
              "description": "Number of results to return per request. Default is 5.",
              "example": "5"
            },
            "required": false,
            "name": "limit",
            "in": "query"
          },
          {
            "schema": {
              "type": "string",
              "description": "Get the next [limit] results starting with this number. Default is 0."
            },
            "required": false,
            "name": "start",
            "in": "query"
          },
          {
            "schema": {
              "type": "string",
              "description": "Term to search on"
            },
            "required": false,
            "name": "q",
            "in": "query"
          },
          {
            "schema": {
              "type": "string",
              "description": "The unique identifier for a gallery."
            },
            "required": false,
            "name": "galleryId",
            "in": "query"
          },
          {
            "schema": {
              "type": "string",
              "description": "The unique identifier for an asset within a gallery."
            },
            "required": false,
            "name": "id",
            "in": "query"
          }
        ],
        "responses": {
          "200": {
            "description": "Returns galleries created by national parks and other NPS entities.",
            "content": {
              "application/json": {
                "schema": {
                  "type": "object",
                  "properties": {
                    "total": {
                      "type": "string",
                      "description": "Total number of results"
                    },
                    "limit": {
                      "type": "string",
                      "description": "Number of results per request"
                    },
                    "start": {
                      "type": "string",
                      "description": "Start position of results"
                    },
                    "data": {
                      "type": "array",
                      "items": {
                        "$ref": "#/components/schemas/Gallery Asset"
                      }
                    }
                  },
                  "required": [
                    "total",
                    "limit",
                    "start",
                    "data"
                  ]
                }
              }
            }
          }
        }
      }
    },
    "/api/thingstodo": {
      "get": {
        "tags": [
          "Things to do"
        ],
        "summary": "Retrieve suggested things to do recommended by and for specific national parks.",
        "operationId": "get_ThingsTodoList",
        "parameters": [
          {
            "schema": {
              "type": "array",
              "items": {
                "type": "string"
              },
              "description": "A comma delimited list of park codes (each 4-10 characters in length)."
            },
            "required": false,
            "name": "parkCode",
            "in": "query"
          },
          {
            "schema": {
              "type": "array",
              "items": {
                "type": "string"
              },
              "description": "A comma delimited list of 2 character state codes.",
              "example": "CA,UT"
            },
            "required": false,
            "name": "stateCode",
            "in": "query"
          },
          {
            "schema": {
              "type": "array",
              "items": {
                "type": "string"
              },
              "description": "A comma delimited list of resource properties to sort the results by. Ascending order is assumed for each property. If descending order is desired, the unary negative should prefix the property name. Invalid property values will be ignored. If no sort parameter is passed in a request, the default sort is by descending order of date last modified. (Note that the date last modified is an unexposed property.) If sorting by relevanceScore, you will likely use -relevanceScore as a higher score indicates a more accurate result. The only sort option, besides the default, is relevanceScore."
            },
            "required": false,
            "name": "sort",
            "in": "query"
          },
          {
            "schema": {
              "type": "string",
              "default": "5",
              "description": "Number of results to return per request. Default is 5.",
              "example": "5"
            },
            "required": false,
            "name": "limit",
            "in": "query"
          },
          {
            "schema": {
              "type": "string",
              "description": "Get the next [limit] results starting with this number. Default is 0."
            },
            "required": false,
            "name": "start",
            "in": "query"
          },
          {
            "schema": {
              "type": "string",
              "description": "Term to search on"
            },
            "required": false,
            "name": "q",
            "in": "query"
          }
        ],
        "responses": {
          "200": {
            "description": "Returns a list of things to do",
            "content": {
              "application/json": {
                "schema": {
                  "type": "object",
                  "properties": {
                    "total": {
                      "type": "string",
                      "description": "Total number of results"
                    },
                    "limit": {
                      "type": "string",
                      "description": "Number of results per request"
                    },
                    "start": {
                      "type": "string",
                      "description": "Start position of results"
                    },
                    "data": {
                      "type": "array",
                      "items": {
                        "type": "object",
                        "properties": {
                          "shortDescription": {
                            "type": "string",
                            "description": "Short description of the thing to do"
                          },
                          "longDescription": {
                            "type": "string",
                            "description": "Long description of the thing to do"
                          },
                          "isReservationRequired": {
                            "type": "string",
                            "description": "Indicates if a reservation is required"
                          },
                          "season": {
                            "type": "array",
                            "items": {
                              "type": "string"
                            }
                          },
                          "topics": {
                            "type": "array",
                            "items": {
                              "type": "object",
                              "properties": {
                                "id": {
                                  "type": "string",
                                  "description": "ID of the topic"
                                },
                                "name": {
                                  "type": "string",
                                  "description": "Name of the topic"
                                }
                              },
                              "required": [
                                "id",
                                "name"
                              ]
                            }
                          },
                          "timeOfDayDescription": {
                            "type": "string",
                            "description": "Description of the time of day"
                          },
                          "locationDescription": {
                            "type": "string",
                            "description": "Location description, for example, details about where the trail head starts"
                          },
                          "petsDescription": {
                            "type": "string",
                            "description": "Pet policy"
                          },
                          "durationDescription": {
                            "type": "string",
                            "description": "Description of the duration"
                          },
                          "latitude": {
                            "type": "string",
                            "description": "Latitude"
                          },
                          "activityDescription": {
                            "type": "string",
                            "description": "Description of the activity"
                          },
                          "activities": {
                            "type": "array",
                            "items": {
                              "$ref": "#/components/schemas/Activity"
                            }
                          },
                          "url": {
                            "type": "string",
                            "description": "URL of the thing to do"
                          },
                          "longitude": {
                            "type": "string",
                            "description": "Longitude"
                          },
                          "reserverationDescription": {
                            "type": "string",
                            "description": "Reservation description"
                          },
                          "arePetsPermitted": {
                            "type": "string",
                            "description": "Indicates if pets are permitted"
                          },
                          "geometryPoiId": {
                            "type": "string",
                            "description": "Id for Geometry Point of Interest"
                          },
                          "duration": {
                            "type": "string",
                            "description": "Duration of the activity"
                          },
                          "location": {
                            "type": "string",
                            "description": "Location of the activity"
                          },
                          "feeDescription": {
                            "type": "string",
                            "description": "Description of the fee"
                          },
                          "doFeesApply": {
                            "type": "string",
                            "description": "Indicates if fees apply"
                          },
                          "title": {
                            "type": "string",
                            "description": "Title of the activity"
                          },
                          "images": {
                            "type": "array",
                            "items": {
                              "type": "object",
                              "properties": {
                                "credit": {
                                  "type": "string",
                                  "description": "Credit for the image"
                                },
                                "altText": {
                                  "type": "string",
                                  "description": "Alternate text for the image"
                                },
                                "title": {
                                  "type": "string",
                                  "description": "Title of the image"
                                },
                                "caption": {
                                  "type": "string",
                                  "description": "Caption for the image"
                                },
                                "url": {
                                  "type": "string",
                                  "description": "URL of the image"
                                },
                                "crops": {
                                  "type": "array",
                                  "items": {
                                    "type": "object",
                                    "properties": {
                                      "aspectratio": {
                                        "type": "number",
                                        "description": "Aspect ratio of the image"
                                      },
                                      "url": {
                                        "type": "string",
                                        "description": "URL of this cropped image"
                                      }
                                    },
                                    "required": [
                                      "aspectratio",
                                      "url"
                                    ]
                                  }
                                }
                              },
                              "required": [
                                "credit",
                                "altText",
                                "title",
                                "caption",
                                "url",
                                "crops"
                              ]
                            }
                          },
                          "timeOfDay": {
                            "type": "array",
                            "items": {
                              "type": "string"
                            },
                            "description": "Time of day"
                          },
                          "tags": {
                            "type": "array",
                            "items": {
                              "type": "string"
                            },
                            "description": "Tags"
                          },
                          "seasonDescription": {
                            "type": "string",
                            "description": "Description of the season"
                          },
                          "relevanceScore": {
                            "type": "number",
                            "description": "The relevance score is a numeric calculation of how much your item meets the criteria of your q (query text) search. This is normally coupled with a sort value of -relevanceScore. A higher value means that your item meets the criteria of the q search with a higher frequency and accuracy."
                          },
                          "id": {
                            "type": "string",
                            "description": "Unique identifier for the thing to do"
                          },
                          "arePetsPermittedwithRestrictions": {
                            "type": "string",
                            "description": "Indicates if pets are permitted with restrictions"
                          },
                          "ageDescription": {
                            "type": "string",
                            "description": "Description of the age"
                          },
                          "relatedParks": {
                            "type": "array",
                            "items": {
                              "$ref": "#/components/schemas/Related Park"
                            }
                          },
                          "accessibilityInformation": {
                            "type": "string",
                            "description": "Accessibility information"
                          },
                          "age": {
                            "type": "string",
                            "description": "Age"
                          }
                        },
                        "required": [
                          "shortDescription",
                          "longDescription",
                          "isReservationRequired",
                          "season",
                          "topics",
                          "timeOfDayDescription",
                          "locationDescription",
                          "petsDescription",
                          "durationDescription",
                          "latitude",
                          "activityDescription",
                          "activities",
                          "url",
                          "longitude",
                          "reserverationDescription",
                          "arePetsPermitted",
                          "geometryPoiId",
                          "duration",
                          "location",
                          "feeDescription",
                          "doFeesApply",
                          "title",
                          "images",
                          "timeOfDay",
                          "tags",
                          "seasonDescription",
                          "relevanceScore",
                          "id",
                          "arePetsPermittedwithRestrictions",
                          "ageDescription",
                          "relatedParks",
                          "accessibilityInformation",
                          "age"
                        ]
                      }
                    }
                  },
                  "required": [
                    "total",
                    "limit",
                    "start",
                    "data"
                  ]
                }
              }
            }
          }
        }
      }
    }
  },
}
```