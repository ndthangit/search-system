import type { Article } from "../types/article";
import {
    Dialog,
    DialogTitle,
    DialogContent,
    DialogActions,
    Typography,
    Button,
    IconButton,
    Box,
} from "@mui/material";
import CloseIcon from "@mui/icons-material/Close";
import OpenInNewIcon from "@mui/icons-material/OpenInNew";
import CalendarTodayIcon from "@mui/icons-material/CalendarToday";

interface ArticleModalProps {
    article: Article | null;
    isOpen: boolean;
    onClose: () => void;
}

export default function ArticleModal({ article, isOpen, onClose }: ArticleModalProps) {
    if (!article) return null;

    function formatDate(dateString: string) {
        if (!dateString) return "";
        try {
            const date = new Date(dateString);
            return date.toLocaleDateString("vi-VN", {
                day: "numeric",
                month: "long",
                year: "numeric",
            });
        } catch {
            return dateString;
        }
    }

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
                {article.title}
                <IconButton onClick={onClose} aria-label="close">
                    <CloseIcon />
                </IconButton>
            </DialogTitle>

            {/* Body */}
            <DialogContent dividers>
                {article.date && (
                    <Box display="flex" alignItems="center" gap={0.5} mb={2} color="text.secondary">
                        <CalendarTodayIcon sx={{ fontSize: 16 }} />
                        <Typography variant="body2">
                            {formatDate(article.date)}
                        </Typography>
                    </Box>
                )}
                <Typography variant="body1" sx={{ whiteSpace: "pre-line" }}>
                    {article.contents || article.summary || "Không có nội dung."}
                </Typography>
            </DialogContent>

            {/* Footer / Actions */}
            <DialogActions sx={{ p: 2 }}>
                <Button onClick={onClose} color="inherit">
                    Đóng
                </Button>
                {article.url && (
                    <Button
                        href={article.url}
                        target="_blank"
                        rel="noopener noreferrer"
                        variant="contained"
                        endIcon={<OpenInNewIcon />}
                    >
                        Xem bài viết
                    </Button>
                )}
            </DialogActions>
        </Dialog>
    );
}
