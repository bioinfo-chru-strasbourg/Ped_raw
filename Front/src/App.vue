<template>
  <div class="nav-scroller py-1">
    <router-link to="/" class="navbar-brand">
      <img src="/logoprov5.png" alt="logo" style="float:left">
    </router-link>
      <div class="d-flex justify-content-between align-items-center" style="">
          <div style="">
              <router-link to="/" class="navbar-brand">
                  <Button class="mb-2" severity="secondary" style="font-size: 3.5rem; color: black; margin-left:1.5rem ;padding-top:0; padding-bottom:0"
                      text>Ped_raw
                  </Button>
              </router-link>
          </div>
          <div style="">
              <router-link to="/" class="navbar-brand">
                  <Button class="mb-2 navbutton" severity="secondary" text>Pedigree</Button>
              </router-link>
              <router-link to="/doc" class="navbar-brand">
                  <Button class="mb-2 navbutton" severity="secondary" text>About</Button>
              </router-link>
              <a href="mailto:bioinfo@chru-strasbourg.fr" class="navbar-brand">
                  <Button class="mb-2 navbutton" severity="secondary" text>Contact us</Button>
              </a>
          </div>
      </div>
      <hr style=" margin-left: 10rem; margin-top: 0.5rem; margin-bottom: 2rem;">
  </div>
  <RouterView />
</template>

<script setup>
import { RouterView } from 'vue-router'
</script>

<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@600&display=swap');


#app {
  /* margin-top: 1rem !important; */
  margin-left: 0.5rem !important;
  margin-right: 0.5rem !important;
  padding: 0.5rem !important;
}

.navbutton {
  /* font-family: 'Playfair Display', serif !important; */
  color: #495978 !important;
  font-size:2rem !important;
}
</style>