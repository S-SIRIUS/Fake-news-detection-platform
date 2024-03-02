
    <script>
        import { push } from 'svelte-spa-router'
        import fastapi from "../lib/api"
        import Error from "../components/Error.svelte"
        import {link} from 'svelte-spa-router'

        let error = {detail:[]}
        let press = ""
        let content = ""
        let ans=undefined
        let Q_ID=""
        let state=0

        function post_question(event) {
            event.preventDefault()
            let url = "/fakenews/question/create"
            let params = {
                press: press,
                content: content,
            }
            fastapi('post', url, params, 
                (json) => {
                    press=''
                    content=''
                    ans=json["Fake"]
                    Q_ID=json['Q_ID']
                },
                (json_error) => {
                    error = json_error
                }
            )
            state=1
        }

    </script>
    <head>
        
        <meta charset="utf-8" />
        <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no" />
        <meta name="description" content="" />
        <meta name="author" content="" />
        <title>Business Frontpage - Start Bootstrap Template</title>
        <!-- Bootstrap icons-->
        <link href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.4.1/font/bootstrap-icons.css" rel="stylesheet" />
    </head>
    <body>
        
        <!-- Header-->
        <header class="bg-dark py-5">
            <div class="container px-5">
                <div class="row gx-5 justify-content-center">
                    <div class="col-lg-6">
                        <div class="text-center my-5">
                            <h1 class="display-5 fw-bolder text-white mb-2">Please Identify FakeNews</h1>
                            <Error error={error}/>
                            {#if ans > 50}
                                <p>FAKE입니다.</p>
                            {:else if ans <50}
                                <p>True입니다.</p>
                            {/if}
                            <div>
                                <form method="post" class="my-3">
                                    <div class="mb-3">
                                        <label for="press">언론사</label>
                                        <!----<input type="text" id="press">--->
                                        <select id="press" bind:value="{press}">
                                            <option value="경향신문">경향신문</option>
                                            <option value="국민일보">국민일보</option>
                                            <option value="동아일보">동아일보</option>
                                            <option value="문화일보">문화일보</option>
                                            <option value="서울신문">서울신문</option>
                                            <option value="세계일보">세계일보</option>
                                            <option value="조선일보">조선일보</option>
                                            <option value="중앙일보">중앙일보</option>
                                            <option value="한겨례">한겨례</option>
                                            <option value="한국일보">한국일보</option>
                                            <option value="한국일보">기타</option>
                                        </select>
                                        <!----<input type="text" class="form-control" bind:value="{press}">-->
                                    </div>
                                    <div class="mb-4">
                                        <label for="content">내용</label>
                                        <textarea class="form-control" rows="10" columns="100" bind:value="{content}"></textarea>
                                    </div>
                                    <button class="btn btn-primary" on:click="{post_question}"><i class="fa-solid fa-magnifying-glass"></i></button>
                                </form>
                                {#if state==1}<!--More Information 나오는 기준-->
                                    <a use:link href="/detail/{Q_ID}">More Information</a>
                                {/if}
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </header>
        <!-- Features section-->
        <section class="py-5 border-bottom" id="features">
            <div class="container px-5 my-5">
                <div class="row gx-5">
                    <div class="col-lg-4 mb-5 mb-lg-0">
                        <div class="feature bg-primary bg-gradient text-white rounded-3 mb-3"><i class="bi bi-collection"></i></div>
                        <h2 class="h4 fw-bolder">AI model</h2>
                        <p>AI모델이 우선적으로 가짜뉴스 여부를 판별해 줍니다. More Information 정보로 들어갈 경우 AI모델이 판별한 가짜뉴스일 가능성을 알 수 있습니다. AI모델이 80퍼센트 이상의 확률로 진짜와 가짜여부를 진단했을 경우 서버에 저장하지 않습니다. 그러나 모델이 30 ~ 70퍼센트 사이로 판별한 데이터는 Notice에 게시됩니다.</p>
    
                    </div>
                    <div class="col-lg-4 mb-5 mb-lg-0">
                        <div class="feature bg-primary bg-gradient text-white rounded-3 mb-3"><i class="bi bi-building"></i></div>
                        <h2 class="h4 fw-bolder">실제 팩트 체커의 이중검증</h2>
                        <p>언론사에서 활동하고 있는 팩트체커만이 사이트에 가입하여 직접 검증을 할 수 있습니다. 팩트 체커는 인공지능 모델이 30~70퍼센트 사이로 판별한 가짜뉴스 데이터에 대한 검증을 수행합니다.</p>
                      
                    </div>
                    <div class="col-lg-4">
                        <div class="feature bg-primary bg-gradient text-white rounded-3 mb-3"><i class="bi bi-toggles2"></i></div>
                        <h2 class="h4 fw-bolder">게시판 기능</h2>
                        <p>팩트체커들은 게시판에서 자신의 검증에 대한 의견을 답글로 토론할 수 있습니다.</p>
                       
                    </div>
                </div>
            </div>
        </section>
       
        <!-- Footer-->
        <footer class="py-5 bg-dark">
            <div class="container px-5"><p class="m-0 text-center text-white">Copyright &copy; CAU 18 자연어처리 크루(강준규, 김민기, 송창욱)</p></div>
        </footer>
        <script src="https://kit.fontawesome.com/e759ba39a0.js" crossorigin="anonymous"></script>
    </body>
