<script>
    import fastapi from "../lib/api"
    import Error from "../components/Error.svelte"
    export let params = {}
    import { link, push } from 'svelte-spa-router'
    import { is_login, username } from "../lib/store"
    import moment from 'moment/min/moment-with-locales'
    moment.locale('ko')
    let question_id = params.question_id  
    let question = {answers:[]}
    let content = ""
    let error = {detail:[]}

    function get_question() {
        fastapi("get", "/fakenews/question/detail/" + question_id, {}, (json) => {
            question = json
        })
    }

    get_question()


    function post_answer(event) {
        event.preventDefault()
        let url = "/fakenews/answer/create/" + question_id
        let params = {
            content: content
        }
        fastapi('post', url, params, 
            (json) => {
                content = ''
                error = {detail:[]}
                get_question()
            },
            (err_json) => {
                error = err_json
            }
        )
    }

    function delete_answer(answer_id) {
        if(window.confirm('정말로 삭제하시겠습니까?')) {
            let url = "/fakenews/answer/delete"
            let params = {
                answer_id: answer_id
            }
            fastapi('delete', url, params, 
                (json) => {
                    get_question()
                },
                (err_json) => {
                    error = err_json
                }
            )
        }
    }


    function vote_answer(answer_id) {
        if(window.confirm('정말로 추천하시겠습니까?')) {
            let url = "/fakenews/answer/vote"
            let params = {
                answer_id: answer_id
            }
            fastapi('post', url, params, 
                (json) => {
                    get_question()
                },
                (err_json) => {
                    error = err_json
                }
            )
        }
    }
</script>
<div class="container my-3">
    <!-- 질문 -->
    <h2 class="border-bottom py-2">{question.press}</h2>
    <p><strong>Fake</strong>일 확률은 {question.fake}% 입니다.</p>
    <p><strong>True</strong>일 확률은 {100-question.fake}% 입니다.</p>
    <div class="card my-3">
        <div class="card-body">
            <div class="card-text" style="white-space: pre-line;">{question.content}</div>
            <div class="d-flex justify-content-end">
                <div class="badge bg-light text-dark p-2">
                    {moment(question.create_date).format("YYYY년 MM월 DD일 hh:mm a")}
                </div>
            </div>
        </div>
    </div>
    <button class="btn btn-secondary" on:click="{() => {
        push('/notice')
    }}">목록으로</button>
    <!-- 답변 목록 -->
    <h5 class="border-bottom my-3 py-2">{question.answers.length}개의 답변이 있습니다.</h5>
    {#each question.answers as answer}
    <div class="card my-3">
        <div class="card-body">
            <div class="card-text" style="white-space: pre-line;">{answer.content}</div>
            <div class="d-flex justify-content-end">
                {#if answer.modify_date }
                <div class="badge bg-light text-dark p-2 text-start mx-3">
                    <div class="mb-2">modified at</div>
                    <div>{moment(answer.modify_date).format("YYYY년 MM월 DD일 hh:mm a")}</div>
                </div>
                {/if}
                <div class="badge bg-light text-dark p-2 text-start">
                    <div class="mb-2">{ answer.user ? answer.user.username : ""}</div>
                    <div>{moment(answer.create_date).format("YYYY년 MM월 DD일 hh:mm a")}</div>
                </div>
            </div>
            <div class="my-3">
                <button class="btn btn-sm btn-outline-secondary"
                    on:click="{vote_answer(answer.id)}"> 
                    추천
                    <span class="badge rounded-pill bg-success">{ answer.voter.length }</span>
                </button>
                {#if answer.user && $username === answer.user.username }
                <a use:link href="/answer-modify/{answer.id}" 
                    class="btn btn-sm btn-outline-secondary">수정</a>
                <button class="btn btn-sm btn-outline-secondary"
                    on:click={() => delete_answer(answer.id) }>삭제</button>
                {/if}
            </div>
        </div>
    </div>
    {/each}
    <!-- 답변 등록 -->
    <Error error={error} />
    <form method="post" class="my-3">
        <div class="mb-3">
            <textarea rows="10" bind:value={content} 
                disabled={$is_login ? "" : "disabled"}
                class="form-control" />
        </div>
        <input type="submit" value="답변등록" class="btn btn-primary {$is_login ? '' : 'disabled'}"on:click="{post_answer}" />
    </form>
</div>

<!---
<h1>{question.press}</h1>
<div>
    {question.content}
</div>
<div>

</div>
<ul>
    {#each question.answers as answer}
        <li>{answer.content}</li>
    {/each}
</ul>
<Error error={error} />
<form method="post">
    <textarea rows="15" bind:value={content}></textarea>
    <input type="submit" value="답변등록" on:click="{post_answer}">
</form>-->