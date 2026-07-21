// <afterimage-trial color="#cc0033" duration="20"></afterimage-trial>
//
// 20-second stare-at-a-saturated-color trial. After the countdown the stage
// switches to a white field for the user to observe the opponent afterimage.

class AfterimageTrial extends HTMLElement {
  static get observedAttributes() { return ['color', 'duration']; }

  connectedCallback() {
    this._state = 'idle';
    this._mount();
    // Reset if user navigates away mid-trial — the timer would otherwise
    // continue running invisibly and the reveal would land on a stale stage.
    this._onVisibility = () => {
      if (document.hidden && this._state === 'staring') this.reset();
    };
    document.addEventListener('visibilitychange', this._onVisibility);
  }

  _mount() {
    this.innerHTML = `<div class="at-host">
      <div class="at-stage at-stage-idle"></div>
      <div class="at-controls">
        <button class="at-start">start trial</button>
        <button class="at-reset" hidden>reset</button>
      </div>
      <div class="at-instructions"></div>
    </div>`;
    this._stage = this.querySelector('.at-stage');
    this._instructions = this.querySelector('.at-instructions');
    this._startBtn = this.querySelector('.at-start');
    this._resetBtn = this.querySelector('.at-reset');
    this._startBtn.addEventListener('click', () => this.start());
    this._resetBtn.addEventListener('click', () => this.reset());
    this._stage.innerHTML = '<div class="at-fixation" style="color:var(--text-muted)">click <em>start trial</em> to begin</div>';
  }

  start() {
    if (this._state !== 'idle') return;
    const color = this.getAttribute('color') || '#cc0033';
    const duration = parseInt(this.getAttribute('duration') || '20', 10);
    this._state = 'staring';
    this._startBtn.hidden = true;
    this._stage.classList.remove('at-stage-idle');
    this._stage.style.background = color;
    this._stage.innerHTML = `<div class="at-fixation">+</div><div class="at-countdown">${duration}</div>`;
    let remaining = duration;
    this._interval = setInterval(() => {
      remaining--;
      if (remaining <= 0) {
        clearInterval(this._interval);
        this._stage.style.background = '#ffffff';
        this._stage.innerHTML =
          '<div class="at-fixation" style="color:#333">+</div>' +
          '<div class="at-reveal-msg">↑ stare at the cross — what color do you see?</div>';
        this._instructions.innerHTML = `You stared at <strong>${color}</strong>. The afterimage you see is its <em>opponent</em>: red → cyan, blue → yellow, green → magenta.`;
        this._resetBtn.hidden = false;
        this._state = 'reveal';
      } else {
        const cd = this.querySelector('.at-countdown');
        if (cd) cd.textContent = remaining;
      }
    }, 1000);
  }

  reset() {
    if (this._interval) clearInterval(this._interval);
    this._state = 'idle';
    this._stage.classList.add('at-stage-idle');
    this._stage.style.background = '';
    this._stage.innerHTML = '<div class="at-fixation" style="color:var(--text-muted)">click <em>start trial</em> to begin</div>';
    this._instructions.textContent = '';
    this._startBtn.hidden = false;
    this._resetBtn.hidden = true;
  }

  disconnectedCallback() {
    if (this._interval) clearInterval(this._interval);
    if (this._onVisibility) document.removeEventListener('visibilitychange', this._onVisibility);
  }
}

customElements.define('afterimage-trial', AfterimageTrial);
