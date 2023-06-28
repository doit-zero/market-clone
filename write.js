const form = document.getElementById('write-form');


const handleSubmitForm = async (event) => {
    event.preventDefault();
    const body = new FormData(form);
    console.log(body);
    body.append("insertAt",new Date().getTime());
    try{
        const res = await fetch('/items',{
            method:"POST",
            body,
        });
        // 등록 누르면 페이지 이동
        const data = await res.json();
        if(data === '200') window.location.pathname = "/";
    } catch (e) {
        console.error("이미지 업로드에 실패했습이다.");
    }
};

form.addEventListener('submit',handleSubmitForm);