import type { Article } from "../types/article";
import {
    Dialog,
    DialogTitle,
    DialogContent,
    DialogActions,
    Typography,
    Button,
    IconButton,
} from "@mui/material";
import CloseIcon from "@mui/icons-material/Close";
import OpenInNewIcon from "@mui/icons-material/OpenInNew";

interface ArticleModalProps {
    article: Article | null;
    isOpen: boolean;
    onClose: () => void;
}

export default function ArticleModal({ article, isOpen, onClose }: ArticleModalProps) {
    if (!article) return null;

    return (
        <Dialog
            open={isOpen}
            onClose={onClose}
            maxWidth="sm"
            fullWidth
            aria-labelledby="article-dialog-title"
        >
            {/* Header */}
            <DialogTitle
                id="article-dialog-title"
                sx={{
                    display: "flex",
                    alignItems: "center",
                    justifyContent: "space-between",
                    fontWeight: 600,
                    pr: 2,
                }}
            >
                {article.name}
                <IconButton onClick={onClose} aria-label="close">
                    <CloseIcon />
                </IconButton>
            </DialogTitle>

            {/* Body */}
            <DialogContent dividers>
                <Typography variant="body1" sx={{ whiteSpace: "pre-line" }}>
                    {article.abstract || "No content available."}
                </Typography>
            </DialogContent>

            {/* Footer / Actions */}
            <DialogActions sx={{ p: 2 }}>
                <Button onClick={onClose} color="inherit">
                    Close
                </Button>
                <Button
                    href={article.url}
                    target="_blank"
                    rel="noopener noreferrer"
                    variant="contained"
                    endIcon={<OpenInNewIcon />}
                >
                    View on Wikipedia
                </Button>
            </DialogActions>
        </Dialog>
    );
}
