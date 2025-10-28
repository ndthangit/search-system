import { useState } from "react";
import {
    Box,
    Button,
    TextField,
    Typography,
    Stack,
} from "@mui/material";

export default function Import() {
    const [title, setTitle] = useState("");
    const [text, setText] = useState("");
    const [index, setIndex] = useState("");
    const [file, setFile] = useState<File | null>(null);

    const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
        const selectedFile = e.target.files?.[0] || null;
        setFile(selectedFile);
    };

    const handleSubmit = () => {
        const payload = {
            title,
            text,
            index: index,
            file,
        };

        console.log("Submit payload:", payload);
        alert("Đã gửi dữ liệu! (xem console)");
    };

    return (
        <Box sx={{ maxWidth: 700, mx: "auto", mt: 6 }}>
            <Box sx={{ p: 4, borderRadius: 3 }}>
                <Typography variant="h5" fontWeight={600} gutterBottom>
                    Import Data
                </Typography>

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



                    <Button variant="outlined" component="label">
                        Upload JSON File
                        <input type="file" accept=".json" hidden onChange={handleFileChange} />
                    </Button>
                    {file && (
                        <Typography variant="body2" color="text.secondary">
                            Selected file: {file.name}
                        </Typography>
                    )}

                    <Button
                        variant="contained"
                        onClick={handleSubmit}
                    >
                        Submit
                    </Button>
                </Stack>
            </Box>
        </Box>
    );
}
