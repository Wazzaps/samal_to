<template>
  <b-avatar :variant="'custom-color-' + person.ident_color" :size="size" :class="{'badge-no-shadow': flat}">
  <!-- <b-icon
      :icon="badgePatternToIcon[person.ident_pattern]"
      :variant="badgeColorToFgVariant[person.ident_color]"
  /> -->
  <strong>{{person.num}}</strong>
  </b-avatar>
</template>

<script>
export default {
  name: "PersonBubble",
  props: {
    person: Object,
    size: {
      type: String,
      default: 'md'
    },
    flat: Boolean,
  }
}
</script>

<style>
.badge-custom-color-0 {
  background: linear-gradient(#C20E20, #AA0C1C);
  box-shadow: 0 3px 12px -2px #AA0C1CEE;
  color: #ffffffee;
}
.badge-custom-color-1 {
  background: linear-gradient(#FFBAA4, #FFAC92);
  box-shadow: 0 3px 12px -2px #c57e68ee;
  color: #000000ee;
}
.badge-custom-color-2 {
  background: linear-gradient(#006ECB, #0063B6);
  box-shadow: 0 3px 12px -2px #006CC7EE;
  color: #ffffffee;
}
.badge-custom-color-3 {
  background: linear-gradient(#FFDBF0, #EEC7D5);
  box-shadow: 0 3px 12px -2px #c7afb3ee;
  color: #000000ee;
}
.badge-custom-color-4 {
  background: linear-gradient(#00675E, #006057);
  box-shadow: 0 3px 12px -2px #00675EEE;
  color: #ffffffee;
}
.badge-custom-color-5 {
  background: linear-gradient(#68E7E5, #42D9D6);
  box-shadow: 0 3px 12px -2px #59b6b4ee;
  color: #000000ee;
}

.badge-custom-color-0,
.badge-custom-color-1,
.badge-custom-color-2,
.badge-custom-color-3,
.badge-custom-color-4,
.badge-custom-color-5 {
  font-family: 'Rubik', sans-serif;
}



.badge-custom-color-0.badge-no-shadow {
  background: #C20E20;
}
.badge-custom-color-1.badge-no-shadow {
  background: #FFBAA4;
}
.badge-custom-color-2.badge-no-shadow {
  background: #006ECB;
}
.badge-custom-color-3.badge-no-shadow {
  background: #FFDBF0;
}
.badge-custom-color-4.badge-no-shadow {
  background: #00675E;
}
.badge-custom-color-5.badge-no-shadow {
  background: #68E7E5;
}

.badge-no-shadow {
  box-shadow: none;
}
</style>