<template><div class="home">
  <a-layout style="height:fit-content">

      <!-- header -->
      <a-layout-header>
        <a-page-header title="simple-expression-corrector" subtitle="v 1.0" :show-back="false">
        <template #extra>
          <a-avatar>未登录</a-avatar>
        </template>
        <div/>
        </a-page-header>
      </a-layout-header>

      <!-- content -->
      <a-layout-content>
        <a-upload style="padding: 20px; width:95%; text-align: left;"
          accept="image/png"
          list-type="picture"
          action="/"
          :default-file-list="imageList"
        >
        <template v-slot:image="{ fileItem }">
          <a-image :src="fileItem.url" width="40" height="40"/>
          <a-button type="primary" size="mini" 
            style="position:absolute; top:15px; right:100px"
            @click="showResult(fileItem)"
          >查看结果</a-button>
        </template>
        </a-upload>
      </a-layout-content>

      <!-- footer -->
      <a-layout-footer>Footer</a-layout-footer>
    </a-layout>

    <!-- result -->
    <a-drawer :visible="resVisible" placement="bottom" @ok="handleOk" @cancel="handleCancel" :hide-cancel="true" unmountOnClose>
    <template #title>
      {{ resTitle }}
    </template>
    <div>{{ resContent }}</div>
  </a-drawer>
</div></template>

<script lang="ts">
import { Options, Vue } from 'vue-class-component'
import HelloWorld from '@/components/HelloWorld.vue'

@Options({
  components: {
    HelloWorld
  }
})
export default class Home extends Vue {
  imageList = [
    {
      uid: '-2',
      name: '20200717-103937.png',
      url: '//p1-arco.byteimg.com/tos-cn-i-uwbnlip3yd/a8c8cdb109cb051163646151a4a5083b.png~tplv-uwbnlip3yd-webp.webp'
    },
    {
      uid: '-1',
      name: 'hahhahahahaha.png',
      url: '//p1-arco.byteimg.com/tos-cn-i-uwbnlip3yd/e278888093bef8910e829486fb45dd69.png~tplv-uwbnlip3yd-webp.webp'
    }
  ]

  resVisible = false
  resTitle = 'Result'
  resContent = 'nothing'

  handleOk ():void {
    this.resVisible = false
  }

  handleCancel = () => {
    this.resVisible = false
  }

  showResult (fileItem: {uid: string, name: string, url: string}): void {
    const title = fileItem.name
    const content = fileItem.uid + ', url = ' + fileItem.url + ', Result = noting'
    this.resVisible = true
    this.resTitle = title
    this.resContent = content
  }
}
</script>
