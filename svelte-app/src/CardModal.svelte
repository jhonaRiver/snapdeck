<script>
  export let card = null;
</script>

{#if card}
  <div class="modal">
    <div class="modal-content">
      <!-- <img src={card.img} alt="Card" /> -->
      <p>{card.ability}</p>
      <button on:click={() => (card = null)}>Close</button>
    </div>
  </div>
{/if}

<style>
  .modal {
    position: fixed;
    z-index: 1;
    left: 0;
    top: 0;
    width: 100%;
    height: 100%;
    overflow: auto;
    background-color: rgba(0, 0, 0, 0.4);
    display: flex;
    justify-content: center;
    align-items: center;
  }
  .modal-content {
    box-sizing: border-box;
    background-color: #fefefe;
    padding: 20px;
    border: 1px solid #888;
    display: flex;
    flex-direction: column;
    align-items: center;
    max-width: 90%;
  }
</style>
