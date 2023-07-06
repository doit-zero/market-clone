<script>
  let hour = new Date().getHours();
  let min = new Date().getMinutes();
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

<footer>
  <div class="footer-block">
    <div class="footer-icons">
      <div class="footer-icons__img">
        <img src="assets/home.svg" alt="" />
      </div>
      <div>홈</div>
    </div>
    <div class="footer-icons">
      <div class="footer-icons__img">
        <img src="assets/life.svg" alt="" />
      </div>
      <div>동네생활</div>
    </div>
    <div class="footer-icons">
      <div class="footer-icons__img">
        <img src="assets/location.svg" alt="" />
      </div>
      <div>내 근처</div>
    </div>
    <a class="footer-icons" href="#/chat">
      <div class="footer-icons__img">
        <img src="assets/chat.svg" alt="" />
      </div>
      <div>채팅</div>
    </a>
    <div class="footer-icons">
      <div class="footer-icons__img">
        <img src="assets/user.svg" alt="" />
      </div>
      <div>나의 당근</div>
    </div>
  </div>
</footer>

<style>
  .info-bar__time {
    color: red;
  }
</style>
