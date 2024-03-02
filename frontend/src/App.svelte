<script>
  import Router from 'svelte-spa-router'
  import Home from "./routes/Home.svelte"
  import Detail from './routes/Detail.svelte'
  import Notice from './routes/Notice.svelte'
  import Navigation from "./components/Navigation.svelte"
  import UserCreate from "./routes/UserCreate.svelte"
  import UserLogin from "./routes/UserLogin.svelte"
  import AnswerModify from "./routes/AnswerModify.svelte"
  const routes={
    '/':Home,
    '/notice':Notice,
    '/detail/:question_id' : Detail,
    '/user-create': UserCreate,
    '/user-login': UserLogin,
    '/answer-modify/:answer_id': AnswerModify,
  }
</script>
<Navigation />
<Router {routes}/>

