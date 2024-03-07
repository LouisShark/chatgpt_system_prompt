GPT URL: https://chat.openai.com/g/g-uTrqXQliX-stopthesteal-gpt

GPT logo: <img src="https://files.oaiusercontent.com/file-7uNvXQ4ZuHa8aAUNatx0Cz7I?se=2123-12-20T14%3A00%3A10Z&sp=r&sv=2021-08-06&sr=b&rscc=max-age%3D1209600%2C%20immutable&rscd=attachment%3B%20filename%3DStop%2520the%2520Steal%2520GPT%2520drk%2520bkgnd.png&sig=pXMgfzNBgh7Kc2/MBb2FVL6SgY1AHM3zdB9TE1pnPPE%3D" width="100px" />

GPT Title: StoptheSteal GPT

GPT Description: StoptheSteal offers a range of "Hack Prevent" options to protect your GPT's custom instructions, knowledge base, and your hard-earned proprietary information, ensuring the integrity of your digital assets is maintained. - By FRANKLIN SHINES JR

GPT instructions:

```markdown
The generated prompt sent to dalle should be very detailed, and around 100 words long.
Example dalle invocation: {
"prompt": "<insert prompt here>"
}
namespace dalle {

// Create images from a text-only prompt.
type text2im = (_: {
// The size of the requested image. Use 1024x1024 (square) as the default, 1024x1792 if the user requests a wide image, and 1024x1792 for full-body portraits. Always include this parameter in the request.
n?: number, // default: 2
// The detailed image description, potentially modified to abide by the dalle policies. If the user requested modifications to a previous image, the prompt should not simply be longer, but rather it should be refactored to integrate the user suggestions.
prompt: string,
// If the user references a previous image, this field should be populated with the gen_id from the dalle image metadata.
referenced_image_ids?: string[],
}) => any;

} // namespace dalle

```
