# Assistants API

[**Assistants API Beta**](https://platform.openai.com/docs/assistants/overview/agents)

The Assistants API allows you to build AI assistants within your own applications. An Assistant has instructions and can leverage models, tools, and knowledge to respond to user queries. The Assistants API currently supports three types of [tools](https://platform.openai.com/docs/assistants/tools): Code Interpreter, Retrieval, and Function calling. In the future, we plan to release more OpenAI-built tools, and allow you to provide your own tools on our platform.

Explore the capabilities of the Assistants API using the [Assistants playground](https://platform.openai.com/playground?mode=assistant) or by building a step-by-step integration outlined in this guide. A typical integration of the Assistants API includes:

1. **Create an Assistant:** Define custom instructions and pick a model for your [Assistant](https://platform.openai.com/docs/api-reference/assistants/createAssistant). Enable tools like Code Interpreter, Retrieval, and Function calling.
2. **Create a Thread:** Start a [Thread](https://platform.openai.com/docs/api-reference/threads) when a user begins a conversation.
3. **Add Messages:** Include [Messages](https://platform.openai.com/docs/api-reference/messages) in the Thread as users ask questions.
4. **Run the Assistant:** Trigger responses by [running](https://platform.openai.com/docs/api-reference/runs) the Assistant on the Thread, automatically calling the relevant tools.

The Assistants API is in **beta**. We welcome your feedback in our [Developer Forum](https://community.openai.com/)!

This starter guide details the key steps to create and run an Assistant using the [Code Interpreter](https://platform.openai.com/docs/assistants/tools/code-interpreter).

### Step 1: Create an Assistant

[**Create an Assistant**](https://platform.openai.com/docs/assistants/overview/step-1-create-an-assistant)

Configure an Assistant to respond to Messages using parameters such as:

- **Instructions:** Define how the Assistant and model should behave or respond.
- **Model:** Choose from GPT-3.5 or GPT-4 models, including fine-tuned ones. The Retrieval tool requires `gpt-3.5-turbo-1106` and `gpt-4-1106-preview` models.
- **Tools:** The API supports built and hosted tools by OpenAI like Code Interpreter and Retrieval.
- **Functions:** Define custom function signatures, similar to the [function calling](https://platform.openai.com/docs/guides/function-calling) feature.

Example: Creating a personal math tutor Assistant with Code Interpreter enabled:

Beta HTTP header for API calls:

textCopy code

`OpenAI-Beta: assistants=v1`

Python example:

```python
assistant = client.beta.assistants.create(     name="Math Tutor",     instructions="You are a personal math tutor. Write and run code to answer math questions.",     tools=[{"type": "code_interpreter"}],     model="gpt-4-1106-preview" )
```

### Step 2: Create a Thread

[**Create a Thread**](https://platform.openai.com/docs/assistants/overview/step-2-create-a-thread)

Create a Thread for each user at the start of the conversation. Include user-specific context and files through Messages.

Python example:

```python
thread = client.beta.threads.create()
```

Threads support unlimited Messages. The API optimizes requests to fit within the maximum context window using techniques like truncation.

### Step 3: Add a Message to a Thread

[**Add a Message to a Thread**](https://platform.openai.com/docs/assistants/overview/step-3-add-a-message-to-a-thread)

Messages contain user's text and optional [files](https://platform.openai.com/docs/assistants/tools/supported-files). Image file support is planned for future updates.

Python example:

```python
message = client.beta.threads.messages.create(     thread_id=thread.id,     role="user",     content="I need to solve the equation `3x + 11 = 14`. Can you help me?" )
```


View added Messages using [list Messages in Thread](https://platform.openai.com/docs/api-reference/messages/listMessages).

### Step 4: Run the Assistant

[**Run the Assistant**](https://platform.openai.com/docs/assistants/overview/step-4-run-the-assistant)

Create a [Run](https://platform.openai.com/docs/api-reference/runs/createRun) for the Assistant to process the Thread and respond to user queries. The Assistant appends Messages with the role `assistant`.

Optional: Pass additional instructions while creating the Run.

Python example:

```python
run = client.beta.threads.runs.create(   thread_id=thread.id,   assistant_id=assistant.id,   instructions="Please address the user as Jane Doe. The user has a premium account." )
```

### Step 5: Display the Assistant's Response

Retrieve the Run's [status](https://platform.openai.com/docs/assistants/how-it-works/run-lifecycle) to check its progress from `queued` to `completed`.

Python example:

```python
run = client.beta.threads.runs.retrieve(   thread_id=thread.id,   run_id=run.id )
```

Retrieve and display Messages added by the Assistant.

Python example:

```python
messages = client.beta.threads.messages.list(   thread_id=thread.id )
```

During this Run, the Assistant added two new Messages to the Thread:

|ROLE|CONTENT|
|---|---|
|`user`|I need to solve the equation `3x + 11 = 14`. Can you help me?|
|`assistant`|Certainly, Jane Doe. To solve the equation `(3x + 11 = 14)` for `(x)`, you'll want to isolate `(x)` on one side of the equation. Here's how you can do that:<br><br>1. Subtract 11 from both sides to get `(3x = 3)`.<br>2. Divide both sides by 3 to solve for `(x)`. Let me calculate the value of `(x)` for you.|
|`assistant`|The solution to the equation `(3x + 11 = 14)` is `(x = 1)`.|

---

Explore the [Run Steps](https://platform.openai.com/docs/api-reference/runs/listRunSteps) of this Run to understand the Assistant's processes and tools.

- - -

# How Assistants Work (Beta)

The Assistants API is designed to help developers build powerful AI assistants capable of performing a variety of tasks.

## Overview

- **Beta Status**: The Assistants API is in beta and we are actively working on adding more functionality. Share your feedback in our Developer Forum!
- **Capabilities**:
1. Assistants can call OpenAI’s **[models](https://platform.openai.com/docs/models)** with specific instructions to tune their personality and capabilities.
2. Assistants can access **multiple tools in parallel**. These can be both OpenAI-hosted tools — like [Code interpreter](https://platform.openai.com/docs/assistants/tools/code-interpreter) and [Knowledge retrieval](https://platform.openai.com/docs/assistants/tools/knowledge-retrieval) — or tools you build / host (via [Function calling](https://platform.openai.com/docs/assistants/tools/function-calling)).
3. Assistants can access **persistent Threads**. Threads simplify AI application development by storing message history and truncating it when the conversation gets too long for the model’s context length. You create a Thread once, and simply append Messages to it as your users reply.
4. Assistants can access **[Files](https://platform.openai.com/docs/assistants/tools/supported-files) in several formats** — either as part of their creation or as part of Threads between Assistants and users. When using tools, Assistants can also create files (e.g., images, spreadsheets, etc) and cite files they reference in the Messages they create.

## Objects

![[Pasted image 20231113112640.png]]

### Assistants Object Architecture Diagram

|OBJECT|WHAT IT REPRESENTS|
|---|---|
|Assistant|Purpose-built AI that uses OpenAI’s models and calls tools|
|Thread|A conversation session between an Assistant and a user|
|Message|A message created by an Assistant or a user|
|Run|An invocation of an Assistant on a Thread|
|Run Step|Detailed steps the Assistant took as part of a Run|

## Creating Assistants

We recommend using OpenAI’s [latest models](https://platform.openai.com/docs/models/gpt-4-and-gpt-4-turbo) with the Assistants API for best results and maximum compatibility with tools.

To get started, creating an Assistant only requires specifying the `model` to use. But you can further customize the behavior of the Assistant:

1. Use the `instructions` parameter to guide the personality of the Assistant and define it’s goals. Instructions are similar to system messages in the Chat Completions API.
2. Use the `tools` parameter to give the Assistant access to up to 128 tools. You can give it access to OpenAI-hosted tools like `code_interpreter` and `retrieval`, or call a third-party tools via a `function` calling.
3. Use the `file_ids` parameter to give the tools like `code_interpreter` and `retrieval` access to files. Files are uploaded using the `File` [upload endpoint](https://platform.openai.com/docs/api-reference/files/create) and must have the `purpose` set to `assistants` to be used with this API.

### Example: Creating a Data Visualizer Assistant

First, upload a file using the Python SDK:

```python
file = client.files.create(
  file=open("speech.py", "rb"),
  purpose='assistants'
)
```

Then, create the Assistant with the uploaded file:

```python
assistant = client.beta.assistants.create(
  name="Data visualizer",
  description="You are great at creating beautiful data visualizations. You analyze data present in .csv files, understand trends, and come up with data visualizations relevant to those trends. You also share a brief text summary of the trends observed.",
  model="gpt-4-1106-preview",
  tools=[{"type": "code_interpreter"}],
  file_ids=[file.id]
)
```

- **Note**: Maximum of 20 files per Assistant, each up to 512 MB. Total file storage not to exceed 100GB. Storage limit increases can be requested via the help center.

## Managing Threads and Messages

Threads and Messages facilitate conversation sessions between an Assistant and a user.

### Creating a Thread with Messages

```python
thread = client.beta.threads.create(
  messages=[
    {
      "role": "user",
      "content": "Create 3 data visualizations based on the trends in this file.",
      "file_ids": [file.id]
    }
  ]
)
```

- **Message Content**: Can include text, images, or files. Currently, user-created messages cannot contain images, but this will be supported in the future.

### Message Annotations

- **Types**:
    - `file_citation`: References to quotes in files used by the Assistant.
    - `file_path`: References to files generated by the Assistant.

### Example: Replacing Model-Generated Substrings with Annotations

```python
# Retrieve the message object
message = client.beta.threads.messages.retrieve(
  thread_id="...",
  message_id="..."
)

# Extract the message content
message_content = message.content[0].text
annotations = message_content.annotations
citations = []

# Iterate over the annotations and add footnotes
for index, annotation in enumerate(annotations):
    # Replace the text with a footnote
    message_content.value = message_content.value.replace(annotation.text, f' [{index}]')

    # Gather citations based on annotation attributes
    if (file_citation := getattr(annotation, 'file_citation', None)):
        cited_file = client.files.retrieve(file_citation.file_id)
        citations.append(f'[{index}] {file_citation.quote} from {cited_file.filename}')
    elif (file_path := getattr(annotation, 'file_path', None)):
        cited_file = client.files.retrieve(file_path.file_id)
        citations.append(f'[{index}] Click <here> to download {cited_file.filename}')
        # Note: File download functionality not implemented above for brevity

# Add footnotes to the end of the message before displaying to user
message_content.value += '\n' + '\n'.join(citations)
```

## Runs and Run Steps

### Creating a Run

```python
run = client.beta.threads.runs.create(
  thread_id=thread.id,
  assistant_id=assistant.id
)
```

By default, a Run will use the `model` and `tools` configuration specified in Assistant object, but you can override most of these when creating the Run for added flexibility:

```python
run = client.beta.threads.runs.create(
  thread_id=thread.id,
  assistant_id=assistant.id,
  model="gpt-4-1106-preview",
  instructions="additional instructions",
  tools=[{"type": "code_interpreter"}, {"type": "retrieval"}]
)
```

Note: `file_ids` associated with the Assistant cannot be overridden during Run creation. You must use the [modify Assistant](https://platform.openai.com/docs/api-reference/assistants/modifyAssistant) endpoint to do this.

**Run Lifecycle**: Includes statuses like queued, in_progress, completed, requires_action, expired, cancelling, cancelled, and failed.
![[Pasted image 20231113112420.png]]


|STATUS|DEFINITION|
|---|---|
|`queued`|When Runs are first created or when you complete the `required_action`, they are moved to a queued status. They should almost immediately move to `in_progress`.|
|`in_progress`|While in_progress, the Assistant uses the model and tools to perform steps. You can view progress being made by the Run by examining the [Run Steps](https://platform.openai.com/docs/api-reference/runs/step-object).|
|`completed`|The Run successfully completed! You can now view all Messages the Assistant added to the Thread, and all the steps the Run took. You can also continue the conversation by adding more user Messages to the Thread and creating another Run.|
|`requires_action`|When using the [Function calling](https://platform.openai.com/docs/assistants/tools/function-calling) tool, the Run will move to a `required_action` state once the model determines the names and arguments of the functions to be called. You must then run those functions and [submit the outputs](https://platform.openai.com/docs/api-reference/runs/submitToolOutputs) before the run proceeds. If the outputs are not provided before the `expires_at` timestamp passes (roughly 10 mins past creation), the run will move to an expired status.|
|`expired`|This happens when the function calling outputs were not submitted before `expires_at` and the run expires. Additionally, if the runs take too long to execute and go beyond the time stated in `expires_at`, our systems will expire the run.|
|`cancelling`|You can attempt to cancel an `in_progress` run using the [Cancel Run](https://platform.openai.com/docs/api-reference/runs/cancelRun) endpoint. Once the attempt to cancel succeeds, status of the Run moves to `cancelled`. Cancellation is attempted but not guaranteed.|
|`cancelled`|Run was successfully cancelled.|
|`failed`|You can view the reason for the failure by looking at the `last_error` object in the Run. The timestamp for the failure will be recorded under `failed_at`.|

**Polling for updates**

In order to keep the status of your run up to date, you will have to periodically [retrieve the Run](https://platform.openai.com/docs/api-reference/runs/getRun) object. You can check the status of the run each time you retrieve the object to determine what your application should do next. We plan to add support for streaming to make this simpler in the near future.

**Thread locks**

When a Run is `in_progress` and not in a terminal state, the Thread is locked. This means that:

- New Messages cannot be added to the Thread.
- New Runs cannot be created on the Thread.

### Run Steps

![[Pasted image 20231113112312.png]]

- **Details**:
    - `message_creation`: Steps for creating Messages.
    - `tool_calls`: Steps for calling tools.

## Data Access Guidance

Currently, assistants, threads, messages, and files created via the API are scoped to the entire organization. As such, any person with API key access to the organization is able to read or write assistants, threads, messages, and files in the organization.

We strongly recommend the following data access controls:

- _Implement authorization._ Before performing reads or writes on assistants, threads, messages, and files, ensure that the end-user is authorized to do so. For example, store in your database the object IDs that the end-user has access to, and check it before fetching the object ID with the API.
- _Restrict API key access._ Carefully consider who in your organization should have API keys and periodically audit this list. API keys enable a wide range of operations including reading and modifying sensitive information, such as messages and files.
- _Create separate accounts._ Consider creating separate accounts / organizations for different applications in order to isolate data across multiple applications.

## Limitations

During this beta, there are several known limitations we are looking to address in the coming weeks and months. We will publish a changelog on this page when we add support for additional functionality.

- Support for streaming output (including Messages and Run Steps).
- Support for notifications to share object status updates without the need for polling.
- Support for DALL·E as a tool.
- Support for user message creation with images.


# Tools (Beta)

Give Assistants access to OpenAI-hosted tools like Code Interpreter and Knowledge Retrieval, or build your own tools using Function calling. Usage of OpenAI-hosted tools comes at an additional fee. Visit our help center article to learn more about how these tools are priced.

The Assistants API is in beta, and we are actively working on adding more functionality. Share your feedback in our Developer Forum!

## Code Interpreter

Code Interpreter allows the Assistants API to write and run Python code in a sandboxed execution environment. This tool can process files with diverse data and formatting, and generate files with data and images of graphs. Code Interpreter allows your Assistant to run code iteratively to solve challenging code and math problems. When your Assistant writes code that fails to run, it can iterate on this code by attempting to run different code until the code execution succeeds.

### Enabling Code Interpreter

To enable Code Interpreter, pass the `code_interpreter` in the tools parameter of the Assistant object:

```python
assistant = client.beta.assistants.create(
  instructions="You are a personal math tutor. When asked a math question, write and run code to answer the question.",
  model="gpt-4-1106-preview",
  tools=[{"type": "code_interpreter"}]
)
```

### Passing Files to Code Interpreter

Code Interpreter can parse data from files at both the Assistant and Thread levels:

- **Assistant Level**:
	```python
# Upload a file with an "assistants" purpose
file = client.files.create(
  file=open("speech.py", "rb"),
  purpose='assistants'
)

# Create an assistant using the file ID
assistant = client.beta.assistants.create(
  instructions="You are a personal math tutor. When asked a math question, write and run code to answer the question.",
  model="gpt-4-1106-preview",
  tools=[{"type": "code_interpreter"}],
  file_ids=[file.id]
)
```
    
- **Thread Level**:
    
```python
thread = client.beta.threads.create(
  messages=[
    {
      "role": "user",
      "content": "I need to solve the equation `3x + 11 = 14`. Can you help me?",
      "file_ids": [file.id]
    }
  ]
)
```
    

### Reading Images and Files Generated by Code Interpreter

- Code Interpreter outputs images and data files.

```python
{
    "id": "msg_OHGpsFRGFYmz69MM1u8KYCwf",
    "object": "thread.message",
    "created_at": 1698964262,
    "thread_id": "thread_uqorHcTs46BZhYMyPn6Mg5gW",
    "role": "assistant",
    "content": [
    {
      "type": "image_file",
      "image_file": {
        "file_id": "file-WsgZPYWAauPuW4uvcgNUGcb"
      }
    }
  ]
  # ...
}
```

- Retrieve generated file content using the Files API:

```python
content = client.files.retrieve_content(file.id)`
```

When Code Interpreter references a file path (e.g., ”Download this csv file”), file paths are listed as annotations. You can convert these annotations into links to download the file:

```json
{
  "id": "msg_3jyIh3DgunZSNMCOORflDyih",
  "object": "thread.message",
  "created_at": 1699073585,
  "thread_id": "thread_ZRvNTPOoYVGssUZr3G8cRRzE",
  "role": "assistant",
  "content": [
    {
      "type": "text",
      "text": {
        "value": "The rows of the CSV file have been shuffled and saved to a new CSV file. You can download the shuffled CSV file from the following link:\n\n[Download Shuffled CSV File](sandbox:/mnt/data/shuffled_file.csv)",
        "annotations": [
          {
            "type": "file_path",
            "text": "sandbox:/mnt/data/shuffled_file.csv",
            "start_index": 167,
            "end_index": 202,
            "file_path": {
              "file_id": "file-oSgJAzAnnQkVB3u7yCoE9CBe"
            }
          }
          ...
```

### Input and Output Logs of Code Interpreter

Inspect code input and outputs logs by listing the steps of a Run:

```python
run_steps = client.beta.threads.runs.steps.list(
  thread_id=thread.id,
  run_id=run.id
)
```

```python
{
  "object": "list",
  "data": [
    {
      "id": "step_DQfPq3JPu8hRKW0ctAraWC9s",
      "object": "thread.run.step",
      "type": "tool_calls",
      "run_id": "run_kme4a442kme4a442",
      "thread_id": "thread_34p0sfdas0823smfv",
      "status": "completed",
      "step_details": {
        "type": "tool_calls",
        "tool_calls": [
          {
            "type": "code",
            "code": {
              "input": "# Calculating 2 + 2\nresult = 2 + 2\nresult",
              "outputs": [
                {
                  "type": "logs",
                  "logs": "4"
                }
                        ...
 }
```

## Knowledge Retrieval

Retrieval augments the Assistant with external knowledge, such as proprietary product information or user-provided documents.

### Enabling Retrieval

Enable Retrieval by passing `retrieval` in the tools parameter:

```python
assistant = client.beta.assistants.create(
  instructions="You are a customer support chatbot. Use your knowledge base to best respond to customer queries.",
  model="gpt-4-1106-preview",
  tools=[{"type": "retrieval"}]
)
```

### Uploading Files for Retrieval

Files can be uploaded and passed at both the Assistant and Thread levels:

```python
# Upload a file with an "assistants" purpose
file = client.files.create(
  file=open("knowledge.pdf", "rb"),
  purpose='assistants'
)

# Add the file to the assistant
assistant = client.beta.assistants.create(
  instructions="You are a customer support chatbot. Use your knowledge base to best respond to customer queries.",
  model="gpt-4-1106-preview",
  tools=[{"type": "retrieval"}],
  file_ids=[file.id]
)

# Thread Level 
message = client.beta.threads.messages.create(
  thread_id=thread.id,
  role="user",
  content="I can't find in the PDF manual how to turn off this device.",
  file_ids=[file.id]
)
```

### Deleting Files

Detach a file from an assistant to remove it from the retrieval index:

```python
file_deletion_status = client.beta.assistants.files.delete(
  assistant_id=assistant.id,
  file_id=file.id
)
```

### File Citations

Convert file paths in a Message to corresponding file downloads using the annotations field.

```python
{
    "id": "msg_3jyIh3DgunZSNMCOORflDyih",
    "object": "thread.message",
    "created_at": 1699073585,
    "thread_id": "thread_ZRvNTPOoYVGssUZr3G8cRRzE",
    "role": "assistant",
    "content": [
      {
        "type": "text",
        "text": {
          "value": "The rows of the CSV file have been shuffled and saved to a new CSV file. You can download the shuffled CSV file from the following link:\n\n[Download Shuffled CSV File](sandbox:/mnt/data/shuffled_file.csv)",
          "annotations": [
            {
              "type": "file_path",
              "text": "sandbox:/mnt/data/shuffled_file.csv",
              "start_index": 167,
              "end_index": 202,
              "file_path": {
                "file_id": "file-oSgJAzAnnQkVB3u7yCoE9CBe"
              }
            }
          ]
        }
      }
    ],
    "file_ids": [
      "file-oSgJAzAnnQkVB3u7yCoE9CBe"
    ],
        ...
  },
```

## Function Calling

Similar to the Chat Completions API, the Assistants API supports function calling.

### Defining Functions

Define functions when creating an Assistant:

```python
assistant = client.beta.assistants.create(
  instructions="You are a weather bot. Use the provided functions to answer questions.",
  model="gpt-4-1106-preview",
  tools=[{
      "type": "function",
    "function": {
      "name": "getCurrentWeather",
      "description": "Get the weather in location",
      "parameters": {
        "type": "object",
        "properties": {
          "location": {"type": "string", "description": "The city and state e.g. San Francisco, CA"},
          "unit": {"type": "string", "enum": ["c", "f"]}
        },
        "required": ["location"]
      }
    }
  }, {
    "type": "function",
    "function": {
      "name": "getNickname",
      "description": "Get the nickname of a city",
      "parameters": {
        "type": "object",
        "properties": {
          "location": {"type": "string", "description": "The city and state e.g. San Francisco, CA"},
        },
        "required": ["location"]
      }
    } 
  }]
)
```

### Reading the Functions Called by the Assistant

Check the status of a Run to identify required actions:

```python
{
  "id": "run_3HV7rrQsagiqZmYynKwEdcxS",
  "object": "thread.run",
  "assistant_id": "asst_rEEOF3OGMan2ChvEALwTQakP",
  "thread_id": "thread_dXgWKGf8Cb7md8p0wKiMDGKc",
  "status": "requires_action",
  "required_action": {
    "type": "submit_tool_outputs",
    "submit_tool_outputs": {
      "tool_calls": [
        {
          "id": "call_Vt5AqcWr8QsRTNGv4cDIpsmA",
          "type": "function",
          "function": {
            "name": "getCurrentWeather",
            "arguments": "{\"location\":\"San Francisco\"}"
          }
        },
        {
          "id": "call_45y0df8230430n34f8saa",
          "type": "function",
          "function": {
            "name": "getNickname",
            "arguments": "{\"location\":\"Los Angeles\"}"
          }
        }
      ]
    }
  },
...
```

### Submitting Functions Outputs

Submit tool output to complete a Run:

```python
run = client.beta.threads.runs.submit_tool_outputs(
  thread_id=thread.id,
  run_id=run.id,
  tool_outputs=[
      {
        "tool_call_id": call_ids[0],
        "output": "22C",
      },
      {
        "tool_call_id": call_ids[1],
        "output": "LA",
      },
    ]
)
```

## Supported Files

|FILE FORMAT|MIME TYPE|CODE INTERPRETER|RETRIEVAL|
|---|---|---|---|
|`.c`|text/x-c|||
|`.cpp`|text/x-c++|||
|`.csv`|application/csv||✓|
|`.docx`|application/vnd.openxmlformats-officedocument.wordprocessingml.document||✓|
|...|...|...|...|