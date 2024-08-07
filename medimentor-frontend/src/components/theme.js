import { createTheme } from "@mui/material/styles";

const theme = createTheme({
  palette: {
    primary: {
      main: "#3f51b5", // Customize the primary color
    },
    secondary: {
      main: "#f50057", // Customize the secondary color
    },
    background: {
      default: "#f5f5f5", // Set a background color
    },
  },
  typography: {
    fontFamily: "Gabarito, Roboto, Arial, sans-serif", // Customize font family
  },
  components: {
    // Customize specific components here
  },
});

export default theme;
