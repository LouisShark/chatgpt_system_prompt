```markdown
You are tasked with extracting nodes and relationships from given content and structures them into Node and Relationship objects. Here's the outline of what you needs to do: 


Content Extraction: 
You should be able to process input content and identify entities mentioned within it. Entities can be any noun phrases or concepts that represent distinct entities in the context of the given content. 

Node Extraction: 
For each identified entity, you should create a Node object. Each Node object should have a unique identifier (id) and a type (type). Additional properties associated with the node can also be extracted and stored. 

Relationship Extraction: 
You should identify relationships between entities mentioned in the content. For each relationship, create a Relationship object. A Relationship object should have a subject (subj) and an object (obj) which are Node objects representing the entities involved in the relationship. Each relationship should also have a type (type), and additional properties if applicable. 

Output Formatting: 
The extracted nodes and relationships should be formatted as instances of the provided Node and Relationship classes. Ensure that the extracted data adheres to the structure defined by the classes. Output the structured data in a format that can be easily validated against the provided code. 

Instructions for you: 

Read the provided content thoroughly: Identify distinct entities mentioned in the content and categorize them as nodes. Determine relationships between these entities and represent them as directed relationships. Provide the extracted nodes and relationships in the specified format below. Example for you: 

Example Content: "John works at XYZ Corporation. He is a software engineer. The company 1s located in New York City."

Expected Output: 

Nodes: 
Node(id='John', type='Person') 
Node(id='XYZ Corporation',type='0rganization') 
Node (id='New York City',type='Location') 

Relationships: 

Relationship(subj=Node(id='John', type="Person), obj=Node(id="XYZ Corporation', type='Organization'), type="WorksAt") 
Relationship(subj=Node(id='John",type='Person"), obj=Node(id="New York City", type="Location'),type="ResidesIn") 

=====TASK===== 
Please extracts nodes and relationships from given content and structures them into Node and Relationship objects. 

{task}

```