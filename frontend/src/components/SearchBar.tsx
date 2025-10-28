import {type ChangeEvent, type FormEvent, useState} from "react";
import { TextField, Button, Box, InputAdornment, IconButton } from "@mui/material";
import ClearIcon from '@mui/icons-material/Clear';
import SearchIcon from '@mui/icons-material/Search';

interface SearchBarProps {
    onSearch: (query: string) => void;
    loading: boolean;
}

export default function SearchBar({ onSearch, loading }: SearchBarProps) {
    const [query, setQuery] = useState("");

    const handleSubmit = (e: FormEvent<HTMLFormElement>) => {
        e.preventDefault();
        if (query.trim()) {
            onSearch(query.trim());
        }
    };

    const handleClear = () => {
        setQuery("");
        onSearch("");
    };

    const handleChange = (e: ChangeEvent<HTMLInputElement>) => {
        setQuery(e.target.value);
    };

    return (
        <Box
            component="form"
            onSubmit={handleSubmit}
            sx={{
                display: "flex",
                alignItems: "center",
                p: 1.5,
                borderRadius: 3,
            }}
        >
            <TextField
                fullWidth
                value={query}
                onChange={handleChange}
                placeholder="Search articles..."
                variant="outlined"
                size="small"
                disabled={loading}
                InputProps={{
                    startAdornment: (
                        <InputAdornment position="start">
                            <SearchIcon color="action" />
                        </InputAdornment>
                    ),
                    endAdornment: query && (
                        <InputAdornment position="end">
                            <IconButton
                                onClick={handleClear}
                                disabled={loading}
                                aria-label="clear search"
                            >
                                <ClearIcon />
                            </IconButton>
                        </InputAdornment>
                    ),
                }}
            />

            <Box sx={{ ml: 2 }}>
                <Button
                    type="submit"
                    variant="contained"
                    color="primary"
                    disabled={loading || !query.trim()}
                    startIcon={<SearchIcon />}
                    sx={{ minWidth: 110 }}
                >
                    {loading ? "Searching..." : "Search"}
                </Button>
            </Box>
        </Box>
    );
}
