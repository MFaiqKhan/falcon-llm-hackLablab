import {
  Box,
  Stack,
  Paper,
  Button,
  useTheme,
  TextField,
  Typography,
  useMediaQuery,
} from "@mui/material";
import { useState } from "react";
import { useReactMediaRecorder } from "react-media-recorder";

const Interact = () => {
  const theme = useTheme();
  const [text, setText] = useState("");
  const isSmallScreen = useMediaQuery(theme.breakpoints.down("sm"));

  const { startRecording, stopRecording, mediaBlobUrl } = useReactMediaRecorder(
    { audio: true }
  );

  const handleSubmitText = () => {
    console.log("Text submitted:", text);
    setText("");
  };

  return (
    <Box
      sx={{
        padding: { md: "100px", xs: "10px" },
        display: "flex",
        flexDirection: "column",
      }}
    >
      <Typography
        mb={5}
        fontWeight="900"
        textAlign="center"
        variant={isSmallScreen ? "h5" : "h3"}
      >
        Try It Out
      </Typography>

      <Box
        sx={{
          display: { md: "flex", xs: "block" },
          justifyContent: "space-evenly",
          alignItems: "center",
        }}
      >
        {/* Audio Input */}
        <Paper
          elevation={3}
          sx={{
            marginBottom: { md: "0px", xs: "10px" },
            display: "flex",
            paddingX: { md: "50px", xs: "10px" },
            paddingY: "20px",
            flexDirection: "column",
            width: { md: "45%", xs: "100%" },
          }}
        >
          <Typography
            textAlign="center"
            variant="h5"
            mb={2}
            sx={{ borderBottom: "1px solid black" }}
          >
            Audio Analyzer
          </Typography>
          <Stack
            direction="row"
            spacing={2}
            justifyContent="center"
            sx={{ marginBottom: "20px" }}
          >
            <Button
              variant="text"
              sx={{
                background: "#AF8CCF",
                color: "white",
                textTransform: "capitalize",
                "&:hover": {
                  background: "#563073",
                },
              }}
              onClick={startRecording}
            >
              Start
            </Button>
            <Button
              variant="text"
              sx={{
                background: "#AF8CCF",
                color: "white",
                textTransform: "capitalize",
                "&:hover": {
                  background: "#563073",
                },
              }}
              onClick={stopRecording}
            >
              Stop
            </Button>
          </Stack>

          <audio style={{ width: "100%" }} src={mediaBlobUrl} controls />
        </Paper>

        {/* Text Input */}
        <Paper
          elevation={3}
          sx={{
            display: "flex",
            paddingX: { md: "50px", xs: "10px" },
            paddingY: "20px",
            flexDirection: "column",
            width: { md: "45%", xs: "100%" },
          }}
        >
          <Typography
            textAlign="center"
            variant="h5"
            mb={1}
            sx={{ borderBottom: "1px solid black" }}
          >
            Text Analyzer
          </Typography>
          <TextField
            label="Enter text"
            value={text}
            onChange={(e) => setText(e.target.value)}
            fullWidth
            variant="outlined"
            margin="normal"
          />
          <Button
            variant="text"
            sx={{
              background: "#AF8CCF",
              color: "white",
              textTransform: "capitalize",
              "&:hover": {
                background: "#563073",
              },
            }}
            onClick={handleSubmitText}
          >
            Submit
          </Button>
        </Paper>
      </Box>
    </Box>
  );
};

export default Interact;

{
  /* <Grid container spacing={3}>
            <Grid item xs={12} sm={6}></Grid>
            <Grid item xs={12} sm={6}>
            </Grid>
          </Grid> */
}

{
  /* <Box mt={4} mb={4}>
        <Typography
          variant={isSmallScreen ? "h5" : "h4"}
          gutterBottom
          align="center"
        >
          Interact Now
        </Typography>

        <Grid container spacing={3}>
          <Grid item xs={12} sm={6}>
            <Paper elevation={3} sx={{ padding: "20px" }}>
              <TextField
                label="Enter text"
                value={text}
                onChange={(e) => setText(e.target.value)}
                fullWidth
                variant="outlined"
                margin="normal"
              />
              <Button
                variant="contained"
                color="primary"
                onClick={handleSubmitText}
              >
                Submit
              </Button>
            </Paper>
          </Grid>

          <Grid item xs={12} sm={6}>
            <Paper elevation={3} sx={{ padding: "20px" }}>
              <Stack
                direction="row"
                spacing={2}
                justifyContent="center"
                sx={{ marginBottom: "20px" }}
              >
                <Button
                  variant="contained"
                  color="primary"
                  onClick={startRecording}
                >
                  Start
                </Button>
                <Button
                  variant="contained"
                  color="secondary"
                  onClick={stopRecording}
                >
                  Stop
                </Button>
              </Stack>

              <audio src={mediaBlobUrl} controls />
            </Paper>
          </Grid>
        </Grid>
      </Box> */
}
