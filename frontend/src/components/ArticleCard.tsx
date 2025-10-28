import type { Article } from "../types/article";
import {
    Card,
    CardActionArea,
    CardContent,
    Typography,
    Link,
} from "@mui/material";

interface ArticleCardProps {
    article: Article;
    onClick?: (article: Article) => void;
}

export default function ArticleCard({ article, onClick }: ArticleCardProps) {
    function truncateAbstract(abstract: string, maxLength: number = 200) {
        if (abstract.length <= maxLength) return abstract;
        return abstract.substring(0, maxLength) + "...";
    }

    return (
        <Card
            elevation={3}
            sx={{
                height: "100%",
                display: "flex",
                flexDirection: "column",
                justifyContent: "space-between",
            }}
        >
            <CardActionArea
                onClick={() => onClick?.(article)}
                sx={{ flexGrow: 1, p: 1.5 }}
            >
                <CardContent>
                    <Typography
                        variant="h6"
                        component="div"
                        gutterBottom
                        sx={{
                            fontWeight: 600,
                            lineHeight: 1.3,
                            mb: 1,
                        }}
                    >
                        {article.name}
                    </Typography>

                    <Typography
                        variant="body2"
                        color="text.secondary"
                        sx={{ mb: 2 }}
                    >
                        {truncateAbstract(article.abstract)}
                    </Typography>
                </CardContent>
            </CardActionArea>

            <CardContent sx={{ pt: 0 }}>
                <Link
                    href={article.url}
                    target="_blank"
                    rel="noopener noreferrer"
                    underline="hover"
                    color="primary"
                    sx={{ fontWeight: 500 }}
                    onClick={(e) => e.stopPropagation()}
                >
                    Read more on Wikipedia →
                </Link>
            </CardContent>
        </Card>
    );
}
