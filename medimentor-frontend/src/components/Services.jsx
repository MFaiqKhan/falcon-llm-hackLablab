import {
  Box,
  List,
  ListItem,
  ListItemIcon,
  ListItemText,
  Paper,
  Typography,
} from "@mui/material";
import CircleIcon from "@mui/icons-material/Circle";

const Services = () => {
  return (
    <Box
      sx={{
        padding: { md: "100px", xs: "30px" },
        display: "flex",
        background: "#DAD9E8",
        flexDirection: "column",
      }}
    >
      <Typography textAlign="center" variant="h3" fontWeight="900" mb={5}>
        Our Services
      </Typography>

      <Box
        sx={{
          display: "flex",
          flexDirection: { md: "row", xs: "column" },
          alignItems: "center",
          justifyContent: "center",
          gap: "50px",
        }}
      >
        <Paper
          elevation={3}
          sx={{
            paddingX: { md: "50px", xs: "10px" },
            paddingY: "20px",
            display: "flex",
            flexDirection: "column",
            justifyContent: "center",
            width: { md: "45%", xs: "100%" },
          }}
        >
          <Typography
            textAlign="center"
            variant="h5"
            mb={5}
            sx={{ borderBottom: "1px solid black" }}
          >
            Audio Analyzer
          </Typography>

          <List>
            <ListItem>
              <ListItemIcon>
                <CircleIcon fontSize="small" sx={{ height: "15px" }} />
              </ListItemIcon>
              <ListItemText primary="Transform spoken symptom descriptions into actionable insights." />
            </ListItem>
            <ListItem>
              <ListItemIcon>
                <CircleIcon fontSize="small" sx={{ height: "15px" }} />
              </ListItemIcon>
              <ListItemText primary="Converts speech into text, analyzes symptoms, and provides potential diagnoses or investigative paths." />
            </ListItem>
            <ListItem>
              <ListItemIcon>
                <CircleIcon fontSize="small" sx={{ height: "15px" }} />
              </ListItemIcon>
              <ListItemText primary="Ideal for training medical students in patient interviewing techniques and enhancing diagnostic accuracy." />
            </ListItem>
          </List>
        </Paper>

        <Paper
          elevation={3}
          sx={{
            paddingX: { md: "50px", xs: "10px" },
            paddingY: "20px",
            textAlign: "center",
            display: "flex",
            flexDirection: "column",
            justifyContent: "center",
            width: { md: "45%", xs: "70&" },
          }}
        >
          <Typography
            textAlign="center"
            variant="h5"
            mb={5}
            sx={{ borderBottom: "1px solid black" }}
          >
            Text Analyzer
          </Typography>

          <List>
            <ListItem>
              <ListItemIcon>
                <CircleIcon fontSize="small" sx={{ height: "15px" }} />
              </ListItemIcon>
              <ListItemText primary="Transform spoken symptom descriptions into actionable insights." />
            </ListItem>
            <ListItem>
              <ListItemIcon>
                <CircleIcon fontSize="small" sx={{ height: "15px" }} />
              </ListItemIcon>
              <ListItemText primary="Converts speech into text, analyzes symptoms, and provides potential diagnoses or investigative paths." />
            </ListItem>
            <ListItem>
              <ListItemIcon>
                <CircleIcon fontSize="small" sx={{ height: "15px" }} />
              </ListItemIcon>
              <ListItemText primary="Ideal for training medical students in patient interviewing techniques and enhancing diagnostic accuracy." />
            </ListItem>
          </List>
        </Paper>
      </Box>
    </Box>
  );
};

export default Services;
