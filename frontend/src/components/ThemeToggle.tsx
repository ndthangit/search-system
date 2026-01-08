import { IconButton, Tooltip } from "@mui/material";
import LightModeIcon from "@mui/icons-material/LightMode";
import DarkModeIcon from "@mui/icons-material/DarkMode";
import { useThemeMode } from "../themes/ThemeContext";

export default function ThemeToggle() {
  const { mode, toggleMode } = useThemeMode();

  return (
    <Tooltip title={mode === "light" ? "Chế độ tối" : "Chế độ sáng"}>
      <IconButton
        onClick={toggleMode}
        sx={{
          color: "text.primary",
          bgcolor: "background.paper",
          border: "1px solid",
          borderColor: mode === "light" ? "#e5e7eb" : "#374151",
          "&:hover": {
            bgcolor: mode === "light" ? "#f3f4f6" : "#374151",
          },
        }}
      >
        {mode === "light" ? <DarkModeIcon /> : <LightModeIcon />}
      </IconButton>
    </Tooltip>
  );
}
