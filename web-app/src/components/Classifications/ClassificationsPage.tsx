import { Box, Typography } from "@mui/material";
import ClassificationManager from "./ClassificationManager";

function ClassificationsPage() {
  return (
    <Box sx={{ width: "100%", maxWidth: "100%", overflow: "hidden" }}>
      <Typography variant="h4" gutterBottom>
        Classifications
      </Typography>

      <ClassificationManager />
    </Box>
  );
}

export default ClassificationsPage;
