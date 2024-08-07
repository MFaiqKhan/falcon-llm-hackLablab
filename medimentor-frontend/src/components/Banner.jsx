import { Typography, Box, useMediaQuery, useTheme } from "@mui/material";

const Banner = () => {
  const theme = useTheme();
  const isMediumScreen = useMediaQuery("(min-width:960px)");
  const isSmallScreen = useMediaQuery(theme.breakpoints.down("sm"));

  return (
    <Box
      sx={{
        height: "100vh",
        width: "100%",
        color: "white",
        background: "#20122B",
        // padding: "10px",
        display: "flex",
        alignItems: "center",
        justifyContent: "space-evenly",
        overflow: "hidden",
      }}
    >
      <Box sx={{ paddingX: { xs: "50px" } }}>
        <Typography
          variant={isSmallScreen ? "h5" : "h2"}
          fontWeight="900"
          gutterBottom
          sx={{
            textAlign: { xs: "center", md: "left" },
          }}
        >
          MediMentor
        </Typography>

        <Typography
          variant={isSmallScreen ? "body1" : "h5"}
          fontStyle="oblique"
          mb={5}
          sx={{
            textAlign: { xs: "center", md: "left" },
          }}
        >
          Your AI-powered medical training and diagnostic assistant
        </Typography>

        <Typography
          variant="body2"
          fontWeight="100"
          mt={10}
          sx={{
            textAlign: { xs: "center", md: "left" },
          }}
        >
          Empowering medical professionals with AI-driven support for training,
          diagnosis, and patient communication, leveraging Falcon&apos;s
          multimodal capabilities to process text, images, and audio.
        </Typography>
      </Box>

      {/* Image */}
      <Box>
        {isMediumScreen && (
          <img
            src="/medicine.svg"
            width={isMediumScreen ? "550" : null}
            height={350}
          />
        )}
      </Box>
    </Box>
  );
};

export default Banner;
