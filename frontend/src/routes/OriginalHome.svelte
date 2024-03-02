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
<div class="container">
    <h2 class="my-3 border-bottom pb-2">Fake News Detection</h2>
    <p>제작자: 산업보안학과 강준규, 김민기, 송창욱</p>
    <p>급격히 증가하는 가짜뉴스를 인공지능 모델이 가짜뉴스일 확률을 알려줍니다.</p>
    <p>인공지능이 확인한 가짜뉴스의 정확도가 40~70% 정도면 팩트체커가 직접 다시 검증하고 코멘트합니다.</p>
    <Error error={error} />
    {#if ans > 50}
        <p>FAKE입니다.</p>
    {:else if ans <50}
        <p>True입니다.</p>
    {/if}
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
        <div class="mb-3">
            <label for="content">내용</label>
            <textarea class="form-control" rows="10" bind:value="{content}"></textarea>
        </div>
        <button class="btn btn-primary" on:click="{post_question}">Ask</button>
    </form>
    {#if state==1}<!--More Information 나오는 기준-->
        <a use:link href="/detail/{Q_ID}">More Information</a>
    {/if}
</div>