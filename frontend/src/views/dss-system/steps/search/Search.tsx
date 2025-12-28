import { useState } from "react";
import {
  Container,
  Typography,
  Box,
  Alert,
  CircularProgress,
  Tabs,
  Tab,
  TextField,
  Button,
  Stack,
  Paper,
} from "@mui/material";
import Editor from "@monaco-editor/react";
import { useSearchArticles } from "./hooks/useSearchArticles.tsx";
import type { Article, SearchParams } from "../../../../types/article.ts";
import ArticleList from "../../../../components/ArticleList.tsx";
import ArticleModal from "../../../../components/ArticleModal.tsx";

export default function Search() {
  const [tab, setTab] = useState(0);
  const [params, setParams] = useState<SearchParams>({
    query: "",
    indexName: "articles",
  });
  const [dslText, setDslText] = useState("{}");
  const [selectedArticle, setSelectedArticle] = useState<Article | null>(null);
  const [isModalOpen, setIsModalOpen] = useState(false);

  const { data, error, isLoading } = useSearchArticles(params);

  const handleSearch = () => {
    const finalParams =
      tab === 1
        ? { ...params, dsl: parseDSL(dslText) }
        : { ...params, dsl: {}, model: "match" };
    setParams(finalParams);
    // refetch();
  };

  const handleArticleClick = (article: Article) => {
    setSelectedArticle(article);
    setIsModalOpen(true);
  };

  const handleCloseModal = () => {
    setIsModalOpen(false);
    setSelectedArticle(null);
  };

  const articles = data?.data || [];

  return (
    <Container maxWidth="md" sx={{ py: 4 }}>
      <Typography variant="h4" textAlign="center" mb={3} fontWeight={600}>
        Elasticsearch Query Console
      </Typography>

      <Paper sx={{ mb: 3, borderRadius: 2 }}>
        <Tabs
          value={tab}
          onChange={(_, newValue) => setTab(newValue)}
          textColor="primary"
          indicatorColor="primary"
          centered
        >
          <Tab label="Simple Search" />
          <Tab label="Advanced Query" />
        </Tabs>
      </Paper>

      {/* Simple Search */}
      {tab === 0 && (
        <Stack spacing={2}>
          <TextField
            label="Search text"
            fullWidth
            variant="outlined"
            value={params.query}
            onChange={(e) => setParams({ ...params, query: e.target.value })}
          />
          <Button
            variant="contained"
            onClick={handleSearch}
            disabled={isLoading}
          >
            {isLoading ? "Searching..." : "Search"}
          </Button>
        </Stack>
      )}

      {/* Advanced Query */}
      {tab === 1 && (
        <Box sx={{ mt: 2 }}>
          {/*<FormControl fullWidth sx={{ mb: 2 }}>*/}
          {/*  <InputLabel>Model</InputLabel>*/}
          {/*  <Select*/}
          {/*    label="Model"*/}
          {/*    onChange={(e) =>*/}
          {/*      setParams({ ...params})*/}
          {/*    }*/}
          {/*  >*/}
          {/*    <MenuItem value="match">Match</MenuItem>*/}
          {/*    <MenuItem value="multi_match">Multi Match</MenuItem>*/}
          {/*    <MenuItem value="bool">Bool</MenuItem>*/}
          {/*    <MenuItem value="function_score">Function Score</MenuItem>*/}
          {/*    <MenuItem value="script_score">Script Score</MenuItem>*/}
          {/*  </Select>*/}
          {/*</FormControl>*/}

          <Editor
            height="300px"
            defaultLanguage="json"
            theme="vs-dark"
            value={dslText}
            onChange={(value) => setDslText(value ?? "{}")}
            options={{
              minimap: { enabled: false },
              fontSize: 14,
              automaticLayout: true,
              scrollbar: { vertical: "hidden" },
            }}
          />

          <Button
            variant="contained"
            fullWidth
            sx={{ mt: 2 }}
            onClick={handleSearch}
            disabled={isLoading}
          >
            {isLoading ? "Running..." : "Run Query"}
          </Button>
        </Box>
      )}

      {error && (
        <Alert severity="error" sx={{ mt: 3 }}>
          Failed to search articles. Please check if backend is running.
        </Alert>
      )}

      {isLoading && (
        <Box textAlign="center" mt={3}>
          <CircularProgress />
        </Box>
      )}

      {!isLoading && (
        <ArticleList
          articles={articles}
          loading={isLoading}
          onArticleClick={handleArticleClick}
        />
      )}

      <ArticleModal
        article={selectedArticle}
        isOpen={isModalOpen}
        onClose={handleCloseModal}
      />
    </Container>
  );
}

function parseDSL(str: string) {
  try {
    return JSON.parse(str);
  } catch {
    return {};
  }
}
