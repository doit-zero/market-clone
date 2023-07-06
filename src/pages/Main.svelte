<script>
  import { onMount } from "svelte";
  import Footer from "../components/Footer.svelte";
  import { getDatabase, ref, onValue } from "firebase/database";

  let hour = new Date().getHours();
  let min = new Date().getMinutes();
  //반응형 변수 값이 바뀌면 자동으로 화면 렌더링 시킴
  $: items = [];

  const calcTime = (timestamp) => {
    const curTime = new Date().getTime() - 9 * 60 * 60 * 1000;
    const time = new Date(curTime - timestamp);
    const hour = time.getHours();
    const minute = time.getMinutes();
    const second = time.getSeconds();

    if (hour > 0) return `${hour}시간 전`;
    else if (minute > 0) return `${minute}분 전`;
    else if (second > 0) return `${second}초 전`;
  };

  //다른데 갔다와도 화면 업데이트 시켜주기
  onMount(() => {
    const db = getDatabase();
    const starCountRef = ref(db, "items/");
    onValue(starCountRef, (snapshot) => {
      const data = snapshot.val();
      items = Object.values(data).reverse();
    });
  });
</script>

<div class="media-info-msg">화면 사이즈를 줄여주세요.</div>
<header>
  <div class="info-bar">
    <div class="info-bar__time">{hour}:{min}</div>
    <div class="info-bar__icons">
      <img src="assets/chart.svg" alt="" />
      <img src="assets/wifi.svg" alt="" />
      <img src="assets/battery.svg" alt="" />
    </div>
  </div>
  <div class="menu-bar">
    <div class="menu-bar__location">
      <div>역삼 3동</div>
      <img src="assets/arrow.svg" alt="" />
    </div>
    <div class="menu-bar__icons">
      <img src="assets/search.svg" alt="" />
      <img src="assets/menu.svg" alt="" />
      <img src="assets/bell.svg" alt="" />
      <div id="alarm" />
    </div>
  </div>
</header>

<main>
  <a class="write-btn" href="#/write">+글쓰기</a>
</main>
{#each items as item}
  <div class="item-list">
    <div class="item-list__img">
      <img src={item.imgUrl} alt={item.price} />
    </div>
    <div class="item-list__info">
      <div class="item-list__info-title">{item.title}</div>
      <div class="item-list__info-price">{item.price}</div>
      <div class="item-list__info-meta">
        {item.place}
        {calcTime(item.insertAt)}
      </div>
      <div>{item.description}</div>
    </div>
  </div>
{/each}

<Footer location="home" />

<style>
  .info-bar__time {
    color: red;
  }
</style>
