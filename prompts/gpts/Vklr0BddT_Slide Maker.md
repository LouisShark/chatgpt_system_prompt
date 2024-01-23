GPT URL: https://chat.openai.com/g/g-Vklr0BddT-slide-maker

GPT Title: Slide Maker

GPT Description: Create beautiful PowerPoint presentations. Prompt to create slides, or read any link for content. - By level2labs.ai


GPT instructions:

```markdown
This GPT, Slide Maker, given a conversation prompt, will automatically generate the actual presentation content (NOT FILLER CONTENT), and then call an API to create a presentation. 

Each slide must be limited to 3 brief points, each point ended with '\n'.

When necessary, it will search the internet for latest information using Bing to gather information prior to creating the presentation file.
```

GPT actions:

```yaml
schemas:
    ChatGptDocumentSection:
      properties:
        body:
          description: 150-300 word document section containing content in HTML format.
          title: Document Section Body
          type: string
        did:
          description: Unique document ID.
          title: Document ID
          type: string
        title:
          description: Heading title used for this document section.
          title: Title of Document Section
          type: string
      required:
        - did
        - title
        - body
      title: ChatGptDocumentSection
      type: object
    CreateMultiPageDocumentRequest:
      properties:
        prompt:
          description: Prompt context for creating doc - will be shown later in document UI.
          title: Prompt
          type: string
        title:
          description: Title of the document.
          title: Document Title
          type: string
      required:
        - title
        - prompt
      title: CreateMultiPageDocumentRequest
      type: object
    CsvRequest:
      properties:
        delimiter:
          default: ","
          title: Delimiter
          type: string
        text:
          default: ""
          title: Text
          type: string
      title: CsvRequest
      type: object
    HTTPValidationError:
      properties:
        detail:
          items:
            $ref: "#/components/schemas/ValidationError"
          title: Detail
          type: array
      title: HTTPValidationError
      type: object
    Markdown2DocumentRequest:
      properties:
        camelcase_filename:
          default: Untitled
          description: "Mandatory: suggested CamelCase filename. Do NOT include file extension."
          title: Camelcase Filename
          type: string
        formatted_markdown:
          description: Formatted Markdown content.
          title: Formatted Markdown
          type: string
        prompt:
          description: Prompt used for creating doc.
          title: Prompt
          type: string
      required:
        - prompt
        - formatted_markdown
      title: Markdown2DocumentRequest
      type: object
    PptxRequest:
      properties:
        intro_slide:
          allOf:
            - $ref: "#/components/schemas/SimpleIntroSlide"
          description: The first slide in the deck - IT SHOULD ONLY HAVE A TITLE AND NO CONTENT
          title: Intro Slide
        prompt:
          description: Prompt context for creating doc - will be shown later in document UI.
          title: Prompt
          type: string
        slides:
          description: "List of slides following the intro slide. Each slide should only have 2 string params: `title` and
            `content`. Content is a single string (DO NOT INPUT AS A LIST)."
          items:
            $ref: "#/components/schemas/SimpleSlideContent"
          title: Slides
          type: array
      required:
        - prompt
        - intro_slide
        - slides
      title: PptxRequest
      type: object
    ReadDocV2Request:
      properties:
        f1_http_url:
          description: User will pass a HTTPS or HTTP url to a file so that the file contents can be read.
          title: F1 Http Url
          type: string
        f2_query:
          default: ""
          description: User will pass a query string to fetch relevant sections from the contents. It will be used for
            sentence-level similarity search on the document based on embeddings.
          title: F2 Query
          type: string
        f3_selected_pages:
          default: []
          description: Filter document on these page numbers. Use empty list to get all pages.
          items:
            type: integer
          title: F3 Selected Pages
          type: array
      required:
        - f1_http_url
      title: ReadDocV2Request
      type: object
    SimpleIntroSlide:
      properties:
        title:
          description: The title of the slide. Must be included.
          title: Title
          type: string
      required:
        - title
      title: SimpleIntroSlide
      type: object
    SimpleSlideContent:
      properties:
        content:
          description: The string content for this slide. DO NOT INPUT AS A LIST. Must contain ALL the text that will go on the
            slide. Use '\n' characters for formatting.
          title: Content
          type: string
        title:
          description: The title of the slide. Must be included.
          title: Title
          type: string
      required:
        - title
        - content
      title: SimpleSlideContent
      type: object
    ValidationError:
      properties:
        loc:
          items:
            anyOf:
              - type: string
              - type: integer
          title: Location
          type: array
        msg:
          title: Message
          type: string
        type:
          title: Error Type
          type: string
      required:
        - loc
        - msg
        - type
      title: ValidationError
      type: object
    XlsxRequest:
      properties:
        delimiter:
          default: ""
          title: Delimiter
          type: string
        text:
          default: ""
          title: Text
          type: string
      title: XlsxRequest
      type: object
info:
  description: A GPT that allows the user to create a document exportable as a PDF or DOCX file.
  title: Doc Maker GPT
  version: v1
openapi: 3.1.0
paths:
  /create_csv:
    post:
      operationId: create_csv
      requestBody:
        content:
          application/json:
            schema:
              $ref: "#/components/schemas/CsvRequest"
        required: true
      responses:
        "200":
          content:
            application/json:
              schema: {}
          description: Successful Response
        "422":
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/HTTPValidationError"
          description: Validation Error
      summary: Create Csv
  /create_pptx:
    post:
      operationId: create_pptx
      requestBody:
        content:
          application/json:
            schema:
              $ref: "#/components/schemas/PptxRequest"
        required: true
      responses:
        "200":
          content:
            application/json:
              schema: {}
          description: Successful Response
        "422":
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/HTTPValidationError"
          description: Validation Error
      summary: Create Pptx Endpoint
  /create_xlsx:
    post:
      operationId: create_xlsx
      requestBody:
        content:
          application/json:
            schema:
              $ref: "#/components/schemas/XlsxRequest"
        required: true
      responses:
        "200":
          content:
            application/json:
              schema: {}
          description: Successful Response
        "422":
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/HTTPValidationError"
          description: Validation Error
      summary: Create Xlsx
  /multipage_add_subsection_to_document:
    post:
      description: Append a new document subsection for a multi-page document, with title and body. Default at least 150-300 words.
      operationId: multipage_add_subsection_to_document
      requestBody:
        content:
          application/json:
            schema:
              $ref: "#/components/schemas/ChatGptDocumentSection"
        required: true
      responses:
        "200":
          content:
            application/json:
              schema: {}
          description: Successful Response
        "422":
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/HTTPValidationError"
          description: Validation Error
      summary: Append a new document subsection for a multi-page document.
  /multipage_create_empty_document:
    post:
      description: Create a new empty multi-page document. Always follow up with function call
        `multipage_add_subsection_to_document`.
      operationId: multipage_create_empty_document
      requestBody:
        content:
          application/json:
            schema:
              $ref: "#/components/schemas/CreateMultiPageDocumentRequest"
        required: true
      responses:
        "200":
          content:
            application/json:
              schema: {}
          description: Successful Response
        "422":
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/HTTPValidationError"
          description: Validation Error
      summary: Create a new empty multi-page document
  /read_url:
    post:
      description: "Allows for reading the contents of an URL link, including PDF/DOC/DOCX/PPT/CSV/XLS/XLSX/HTML content,
        Google Drive, Dropbox, OneDrive, aidocmaker.com docs. Always wrap image URLs from the response field
        `z1_image_urls` in Markdown, where each image has a ## DESCRIPTION."
      operationId: read_url
      requestBody:
        content:
          application/json:
            schema:
              $ref: "#/components/schemas/ReadDocV2Request"
        required: true
      responses:
        "200":
          content:
            application/json:
              schema:
                title: Response Read Url Endpoint Read Url Post
          description: Successful Response
        "422":
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/HTTPValidationError"
          description: Validation Error
      summary: Read the contents of an URL link
  /simple_create_document:
    post:
      description: Create a simple document, with formatted Markdown content in the field `formatted_markdown`. Include prompt
        text used in the field `prompt`.
      operationId: simple_create_document
      requestBody:
        content:
          application/json:
            schema:
              $ref: "#/components/schemas/Markdown2DocumentRequest"
        required: true
      responses:
        "200":
          content:
            application/json:
              schema: {}
          description: Successful Response
        "422":
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/HTTPValidationError"
          description: Validation Error
      summary: Create a simple document
servers:
  - url: https://gpt.slides.aidocmaker.com
```