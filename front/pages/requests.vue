<template>
  <v-layout
    column
    justify-center
    align-center
  >
    <v-card>
      <v-card-title>
        クロール要求一覧
        <v-spacer />
        <v-text-field
          v-model="search"
          append-icon="mdi-magnify"
          label="検索"
          sigle-line
        />
      </v-card-title>
      <v-data-table
        :headers="headers"
        :items="requests"
        :items-per-page="5"
        :search="search"
        sort-by="id"
        :sort-desc="true"
        class="elevation-1"
      >
      </v-data-table>
    </v-card>
  </v-layout>
</template>

<script>
import requests from "~/apollo/queries/requests.gql";

export default {
  data () {
    return {
      search: '',
      requests: [],
      headers: [
        { text: 'ID', value: 'id' },
        { text: 'クロール種別', value: 'jobType' },
        { text: '取得元URL', value: 'startUrls' },
        { text: 'スケジュール', value: 'scheduleType' },
      ],
    }
  },
  apollo: {
    requests: {
      prefetch: true,
      query: requests
    },
  }
}
</script>