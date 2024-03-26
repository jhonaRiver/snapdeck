<script>
  import CardModal from "./CardModal.svelte";

  let cardName = "";
  let recommendedCards = [];
  let selectedCard = null;

  async function getRecommendations() {
    const response = await fetch(
      `http://localhost:5000/recommendations?cardName=${cardName}`
    );
    recommendedCards = await response.json();
  }

  async function selectCard(cardName) {
    const response = await fetch(
      `http://localhost:5000/card?cardName=${cardName}`
    );
    const data = await response.json();
    selectedCard = data;
  }
</script>

<div>
  <input bind:value={cardName} placeholder="Enter card name" />
  <button on:click={getRecommendations}>Get Recommendations</button>
</div>

{#if recommendedCards.length > 0}
  <h2>Recommended Deck:</h2>
  <div class="grid">
    {#each recommendedCards as card (card)}
      <img src={card.img} alt="Card" on:click={() => selectCard(card.name)} />
    {/each}
  </div>
{/if}

<CardModal bind:card={selectedCard} />

<style>
  .grid {
    display: grid;
    grid-template-columns: repeat(6, 1fr);
    grid-template-rows: repeat(2, 1fr);
    gap: 10px;
  }
  img {
    width: 100%;
    height: auto;
  }
  h2 {
    color: whitesmoke;
    font-size: 2em;
    font-weight: bold;
  }
</style>
