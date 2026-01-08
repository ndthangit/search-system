import { useState } from "react";
import {
  Container,
  Typography,
  Box,
  Alert,
  TextField,
  Button,
  Paper,
  Select,
  MenuItem,
  FormControl,
  InputAdornment,
  useTheme,
  Pagination,
} from "@mui/material";
import SearchIcon from "@mui/icons-material/Search";
import NewspaperIcon from "@mui/icons-material/Newspaper";
import { useSearchArticles } from "./hooks/useSearchArticles.tsx";
import type { Article, SearchParams } from "../../../../types/article.ts";
import ArticleList from "../../../../components/ArticleList.tsx";
import ThemeToggle from "../../../../components/ThemeToggle.tsx";

const FIELD_OPTIONS = [
  { value: ["title", "link", "summary"], label: "Tất cả" },
  { value: ["title"], label: "Tiêu đề" },
  { value: ["link"], label: "Đường dẫn" },
  { value: ["summary"], label: "Tóm tắt" },
];

export default function Search() {
  const [searchQuery, setSearchQuery] = useState("");
  const [selectedField, setSelectedField] = useState(FIELD_OPTIONS[0].value);
  const [currentPage, setCurrentPage] = useState(1);
  const [params, setParams] = useState<SearchParams>({
    query: "",
    fields: [],
    indexName: "articles",
    page: 1,
    size: 10,
  });

  const theme = useTheme();
  const isDark = theme.palette.mode === "dark";

  const { data, error, isLoading } = useSearchArticles(params);

  const handleSearch = () => {
    if (searchQuery.trim()) {
      setCurrentPage(1);
      setParams({
        query: searchQuery.trim(),
        fields: selectedField ?? [],
        indexName: "articles-json",
        page: 1,
        size: 10,
      });
    }
  };

  const handlePageChange = (_event: React.ChangeEvent<unknown>, page: number) => {
    setCurrentPage(page);
    setParams((prev) => ({
      ...prev,
      page: page,
    }));
  };

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === "Enter") {
      handleSearch();
    }
  };

  // Transform API response to Article format
  const articles: Article[] =
    data?.data?.map((item) => ({
      id: item.id || "",
      title: item.source.title_va || item.source.title_vska,
      summary: item.source.summary_va || "",
      url: item.source.link || "",
      date: item.source.last_updated
        ? new Date(item.source.last_updated).toISOString()
        : "",
    })) || [];

  const totalResults = data?.totalElements ?? (data ? 0 : undefined);
  const searchTime = data?.took;
  const totalPages = data?.totalPages ?? 0;

  return (
    <Container maxWidth="md" sx={{ py: 4, position: "relative" }}>
      {/* Theme Toggle - Top Right */}
      <Box sx={{ position: "absolute", top: 16, right: 16 }}>
        <ThemeToggle />
      </Box>

      {/* Header */}
      <Box textAlign="center" mb={4}>
        <Box
          display="flex"
          alignItems="center"
          justifyContent="center"
          gap={1.5}
          mb={1}
        >
          <NewspaperIcon sx={{ fontSize: 40, color: "primary.main" }} />
          <Typography
            variant="h3"
            fontWeight={700}
            color="primary.main"
            sx={{ letterSpacing: "-0.5px" }}
          >
            Tìm kiếm Báo chí
          </Typography>
        </Box>
        <Typography variant="body1" color="text.secondary">
          Tra cứu thông tin từ hàng ngàn bài báo và tin tức
        </Typography>
      </Box>

      {/* Search Bar */}
      <Paper
        elevation={0}
        sx={{
          p: 2,
          mb: 3,
          borderRadius: 3,
          backgroundColor: isDark ? "background.paper" : "#f0f4ff",
          border: isDark ? "1px solid #374151" : "none",
          display: "flex",
          alignItems: "center",
          gap: 2,
        }}
      >
        <TextField
          fullWidth
          placeholder="search query"
          value={searchQuery}
          onChange={(e) => setSearchQuery(e.target.value)}
          onKeyPress={handleKeyPress}
          variant="outlined"
          size="medium"
          InputProps={{
            startAdornment: (
              <InputAdornment position="start">
                <SearchIcon color="action" />
              </InputAdornment>
            ),
          }}
          sx={{
            backgroundColor: isDark ? "#0f172a" : "white",
            borderRadius: 2,
            "& .MuiOutlinedInput-root": {
              borderRadius: 2,
              "& fieldset": {
                borderColor: isDark ? "#374151" : "#3b82f6",
              },
              "&:hover fieldset": {
                borderColor: isDark ? "#4b5563" : "#2563eb",
              },
              "&.Mui-focused fieldset": {
                borderColor: isDark ? "#60a5fa" : "#1d4ed8",
              },
            },
          }}
        />

        <FormControl sx={{ minWidth: 140 }}>
          <Select
            value={selectedField}
            onChange={(e) => setSelectedField(e.target.value as string[])}
            displayEmpty
            size="medium"
            sx={{
              backgroundColor: isDark ? "#0f172a" : "white",
              borderRadius: 2,
              "& .MuiOutlinedInput-notchedOutline": {
                borderColor: isDark ? "#374151" : "#e0e0e0",
              },
              "&:hover .MuiOutlinedInput-notchedOutline": {
                borderColor: isDark ? "#4b5563" : "#bdbdbd",
              },
            }}
          >
            {FIELD_OPTIONS.map((option) => (
              <MenuItem key={option.label} value={option.value}>
                {option.label}
              </MenuItem>
            ))}
          </Select>
        </FormControl>

        <Button
          variant="contained"
          onClick={handleSearch}
          disabled={isLoading || !searchQuery.trim()}
          sx={{
            minWidth: 120,
            height: 56,
            borderRadius: 2,
            textTransform: "none",
            fontSize: "1rem",
            fontWeight: 600,
          }}
        >
          {isLoading ? "Đang tìm..." : "Tìm kiếm"}
        </Button>
      </Paper>

      {/* Error Alert */}
      {error && (
        <Alert severity="error" sx={{ mb: 3, borderRadius: 2 }}>
          Không thể tìm kiếm bài viết. Vui lòng kiểm tra kết nối backend.
        </Alert>
      )}

      {/* Results */}
      <ArticleList
        articles={articles}
        loading={isLoading}
        totalResults={totalResults}
        searchTime={searchTime}
      />

      {/* Pagination */}
      {totalPages > 1 && (
        <Box display="flex" justifyContent="center" mt={3}>
          <Pagination
            count={totalPages}
            page={currentPage}
            onChange={handlePageChange}
            color="primary"
            size="large"
            showFirstButton
            showLastButton
            sx={{
              "& .MuiPaginationItem-root": {
                borderRadius: 2,
              },
            }}
          />
        </Box>
      )}
    </Container>
  );
}
