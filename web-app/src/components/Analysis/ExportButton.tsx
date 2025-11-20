import { useState } from "react";
import {
  Button,
  Menu,
  MenuItem,
  ListItemIcon,
  ListItemText,
  CircularProgress,
} from "@mui/material";
import DownloadIcon from "@mui/icons-material/Download";
import TableChartIcon from "@mui/icons-material/TableChart";
import { format } from "date-fns";

interface ExportButtonProps {
  dateRange: {
    start_date: string;
    end_date: string;
  };
  viewMode: "analysis" | "complete";
  onExport?: (format: "csv") => Promise<void>;
}

function ExportButton({ dateRange, viewMode, onExport }: ExportButtonProps) {
  const [anchorEl, setAnchorEl] = useState<null | HTMLElement>(null);
  const [isExporting, setIsExporting] = useState(false);
  const open = Boolean(anchorEl);

  const handleClick = (event: React.MouseEvent<HTMLElement>) => {
    setAnchorEl(event.currentTarget);
  };

  const handleClose = () => {
    setAnchorEl(null);
  };

  const handleExportCSV = async () => {
    setIsExporting(true);
    try {
      if (onExport) {
        await onExport("csv");
      } else {
        // Default CSV export logic
        await exportToCSV();
      }
    } catch (error) {
      console.error("Export failed:", error);
    } finally {
      setIsExporting(false);
      handleClose();
    }
  };

  const exportToCSV = async () => {
    // This is a basic implementation - you can enhance it with actual API data
    const filename = `financial-analysis-${format(new Date(), "yyyy-MM-dd")}.csv`;

    // Placeholder CSV content - in a real implementation, this would come from your API
    const csvContent = [
      ["Financial Analysis Export"],
      [`Date Range: ${dateRange.start_date} to ${dateRange.end_date}`],
      [`Mode: ${viewMode}`],
      [`Export Date: ${format(new Date(), "yyyy-MM-dd HH:mm:ss")}`],
      [],
      ["Category", "Type", "Amount", "Count", "Percentage"],
      // Data rows would be added here from your analysis data
    ]
      .map((row) => row.join(","))
      .join("\n");

    // Create and trigger download
    const blob = new Blob([csvContent], { type: "text/csv;charset=utf-8;" });
    const link = document.createElement("a");
    const url = URL.createObjectURL(blob);
    link.setAttribute("href", url);
    link.setAttribute("download", filename);
    link.style.visibility = "hidden";
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
  };

  return (
    <>
      <Button
        variant="outlined"
        startIcon={isExporting ? <CircularProgress size={20} /> : <DownloadIcon />}
        onClick={handleClick}
        disabled={isExporting}
      >
        Export
      </Button>
      <Menu anchorEl={anchorEl} open={open} onClose={handleClose}>
        <MenuItem onClick={handleExportCSV} disabled={isExporting}>
          <ListItemIcon>
            <TableChartIcon fontSize="small" />
          </ListItemIcon>
          <ListItemText>Export as CSV</ListItemText>
        </MenuItem>
      </Menu>
    </>
  );
}

export default ExportButton;
