import { ThemeProvider } from "@mui/material/styles";
import Banner from "./components/Banner";
import Services from "./components/Services";
import theme from "./components/theme";
import { CssBaseline } from "@mui/material";
import Interact from "./components/Interact";

const App = () => {
  return (
    <ThemeProvider theme={theme}>
      <CssBaseline />
      <Banner />
      <Services />
      <Interact />
    </ThemeProvider>
  );
};

export default App;
