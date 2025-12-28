import { useState } from "react";
import {
  Box,
  Button,
  TextField,
  Typography,
  Stack,
  Tabs,
  Tab,
  MenuItem,
  Paper,
} from "@mui/material";
import Editor from "@monaco-editor/react";

export default function FormInput() {
  const [tab, setTab] = useState(0);
  const [title, setTitle] = useState("");
  const [text, setText] = useState("");
  const [index, setIndex] = useState("");
  const [file, setFile] = useState<File | null>(null);
  const [tokenizer, setTokenizer] = useState("standard");
  const [analyzer, setAnalyzer] = useState("default");
  const [rawBody, setRawBody] = useState(`{
      "title": "Example",
      "content": "Hello Elasticsearch"
    }`);

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const selectedFile = e.target.files?.[0] || null;
    setFile(selectedFile);
  };

  const handleSubmit = () => {
    const payload =
      tab === 0
        ? { title, text, index, tokenizer, analyzer, file }
        : { raw: rawBody };
    console.log("Submit payload:", payload);
  };

  return (
    <Box sx={{ maxWidth: 900, mx: "auto", mt: 6 }}>
      <Paper
        elevation={4}
        sx={{
          p: 4,
          borderRadius: 3,
          backdropFilter: "blur(8px)",
        }}
      >
        <Typography variant="h5" fontWeight={600} gutterBottom>
          Elasticsearch Import Console
        </Typography>

        <Tabs
          value={tab}
          onChange={(_, newValue) => setTab(newValue)}
          textColor="primary"
          indicatorColor="primary"
          sx={{ mb: 3 }}
        >
          <Tab label="Basic Import" />
          <Tab label="Advanced (Raw JSON)" />
        </Tabs>

        {tab === 0 && (
          <Stack spacing={3}>
            <TextField
              label="Index"
              fullWidth
              value={index}
              onChange={(e) => setIndex(e.target.value)}
            />
            <TextField
              label="Title"
              fullWidth
              value={title}
              onChange={(e) => setTitle(e.target.value)}
            />
            <TextField
              label="Text Content"
              fullWidth
              multiline
              minRows={4}
              value={text}
              onChange={(e) => setText(e.target.value)}
            />

            <Stack direction="row" spacing={2}>
              <TextField
                select
                label="Tokenizer"
                value={tokenizer}
                onChange={(e) => setTokenizer(e.target.value)}
                sx={{ flex: 1 }}
              >
                <MenuItem value="standard">standard</MenuItem>
                <MenuItem value="whitespace">whitespace</MenuItem>
                <MenuItem value="keyword">keyword</MenuItem>
                <MenuItem value="custom">custom</MenuItem>
              </TextField>

              <TextField
                select
                label="Analyzer"
                value={analyzer}
                onChange={(e) => setAnalyzer(e.target.value)}
                sx={{ flex: 1 }}
              >
                <MenuItem value="default">default</MenuItem>
                <MenuItem value="simple">simple</MenuItem>
                <MenuItem value="stop">stop</MenuItem>
                <MenuItem value="custom">custom</MenuItem>
              </TextField>
            </Stack>

            <Button variant="outlined" component="label">
              Upload JSON File
              <input type="file" accept=".json" hidden onChange={handleFileChange} />
            </Button>
            {file && (
              <Typography variant="body2" color="text.secondary">
                Selected file: {file.name}
              </Typography>
            )}
          </Stack>
        )}

        {tab === 1 && (
          <Box sx={{ mt: 2 }}>
            <Typography
              variant="subtitle1"
              sx={{ mb: 1, color: "text.secondary" }}
            >
              Raw JSON Body
            </Typography>
            <Editor
              height="300px"
              defaultLanguage="json"
              theme="vs-dark"
              value={rawBody}
              onChange={(value) => setRawBody(value || "")}
              options={{
                fontSize: 14,
                minimap: { enabled: false },
                scrollBeyondLastLine: false,
                lineNumbers: "on",
                roundedSelection: false,
                formatOnPaste: true,
                formatOnType: true,
                tabSize: 2,
              }}
            />
          </Box>
        )}

        <Box sx={{ textAlign: "right", mt: 4 }}>
          <Button
            variant="contained"
            color="primary"
            size="large"
            onClick={handleSubmit}
            sx={{ px: 4 }}
          >
            Submit
          </Button>
        </Box>
      </Paper>
    </Box>
  );
}
