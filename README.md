# Venn Diagram Generator - Replicate Model

This is a Cog-packaged Venn diagram generator that can be deployed on Replicate.

## Prerequisites

1. **Install Docker** - [Get Docker](https://docs.docker.com/get-docker/)
2. **Install Cog** - Run these commands:
   ```bash
   sudo curl -o /usr/local/bin/cog -L https://github.com/replicate/cog/releases/latest/download/cog_`uname -s`_`uname -m`
   sudo chmod +x /usr/local/bin/cog
   ```
3. **Create a Replicate account** - Sign up at [replicate.com](https://replicate.com)

## File Structure

```
venn-diagram/
├── cog.yaml          # Defines dependencies and environment
├── predict.py        # Defines the prediction interface
└── README.md         # This file
```

## Test Locally

Run a prediction locally to test your model:

```bash
cog predict -i left_label="Fruits" -i middle_label="Sweet" -i right_label="Red"
```

With custom format and DPI:

```bash
cog predict -i left_label="Python" -i middle_label="JavaScript" -i right_label="TypeScript" -i export_format="svg"
```

For PNG with high DPI:

```bash
cog predict -i left_label="Dogs" -i middle_label="Cats" -i right_label="Birds" -i export_format="png" -i dpi=600
```

## Use Your Model

You can run predictions via:

### Python

```python
import replicate

output = replicate.run(
    "unityaisolutions/venn-diagram:version-id",
    input={
        "left_label": "Fruits",
        "middle_label": "Sweet",
        "right_label": "Red",
        "export_format": "png",
        "dpi": 300
    }
)

# Save the output
with open('venn_diagram.png', 'wb') as f:
    f.write(output.read())
```

### cURL

```bash
curl -s -X POST \
  -H "Authorization: Token $REPLICATE_API_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "version": "your-version-id",
    "input": {
      "left_label": "Fruits",
      "middle_label": "Sweet", 
      "right_label": "Red",
      "export_format": "png"
    }
  }' \
  https://api.replicate.com/v1/predictions
```

### Node.js

```javascript
import Replicate from "replicate";

const replicate = new Replicate({
  auth: process.env.REPLICATE_API_TOKEN,
});

const output = await replicate.run(
  "unityaisolutions/venn-diagram:version-id",
  {
    input: {
      left_label: "Fruits",
      middle_label: "Sweet",
      right_label: "Red",
      export_format: "png",
      dpi: 300
    }
  }
);

console.log(output);
```

## Model Inputs

- `left_label` (string): Label for the left circle (default: "Set A")
- `middle_label` (string): Label for the middle circle (default: "Set B")
- `right_label` (string): Label for the right circle (default: "Set C")
- `export_format` (string): Output format - "png" or "svg" (default: "png")
- `dpi` (integer): DPI for PNG output, 72-600 (default: 300, ignored for SVG)

## Model Output

Returns a `Path` object pointing to the generated Venn diagram file in the specified format.

## Development

To make changes:

1. Edit `predict.py` to modify the prediction logic
2. Edit `cog.yaml` to change dependencies
3. Test locally with `cog predict`
4. Push updates with `cog push` (if you make a commit, we'll do this part for you)

## Support

For issues or questions:
- [Cog Documentation](https://github.com/replicate/cog)
- [Replicate Documentation](https://replicate.com/docs)
- [Replicate Community](https://replicate.com/community)