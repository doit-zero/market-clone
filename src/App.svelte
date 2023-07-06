<script>
  import Login from "./pages/Login.svelte";
  import Main from "./pages/Main.svelte";
  import Signup from "./pages/Signup.svelte";
  import Write from "./pages/Write.svelte";
  import Chat from "./pages/Chat.svelte";
  import Router from "svelte-spa-router";
  import "./css/style.css";
  const routes = {
    "/": Main,
    "/write": Write,
    "/login": Login,
    "/signup": Signup,
    "/chat": Chat,
  };
</script>

<Router {routes} />
