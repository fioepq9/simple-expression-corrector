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
          :custom-request="upload"
          :file-list="imageList"
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
      <a-layout-footer>
        <!-- test -->
        footer
      </a-layout-footer>
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
import axios, { AxiosResponse, Canceler } from 'axios'
import { FileItem, RequestOption, UploadRequest } from '@arco-design/web-vue'

@Options({
  components: {
    HelloWorld
  }
})
export default class Home extends Vue {
  imageList = [] as FileItem[]

  resVisible = false
  resTitle = 'Result'
  resContent = 'nothing'

  handleOk = (): void => {
    this.resVisible = false
  }

  handleCancel = (): void => {
    this.resVisible = false
  }

  showResult = (fileItem: {uid: string, name: string, url: string}): void => {
    const title = fileItem.name
    const content = fileItem.uid + ', url = ' + fileItem.url + ', Result = noting'
    this.resVisible = true
    this.resTitle = title
    this.resContent = content
  }

  upload = (option: RequestOption): UploadRequest => {
    const { onProgress, onError, onSuccess, fileItem, name } = option

    const formData = new FormData()
    formData.append(name as string || 'file', fileItem.file as Blob)

    let cancel: Canceler

    axios.post('http://localhost:8080/api/upload', formData, {
      headers: { 'Content-Type': 'multipart/form-data' },
      onUploadProgress: (process) => {
        let percent = 0
        if (process.total > 0) {
          percent = (process.loaded / process.total) * 100
        }
        onProgress(percent, process)
      },
      cancelToken: new axios.CancelToken((c) => {
        cancel = c
      })
    }).catch((err) => {
      onError(err)
    }).then((vhttpResp: void | AxiosResponse) => {
      // check resp is not null
      if (!vhttpResp) {
        onError('null')
      }
      // parse resp
      const httpResp = vhttpResp as AxiosResponse
      const httpStatus = {
        code: httpResp.status,
        msg: httpResp.statusText
      }
      const resp = httpResp.data
      // check http status
      if (httpStatus.code !== 200) {
        onError(httpStatus.msg)
      }
      // check server status
      if (resp.status.code !== 0) {
        onError(resp.status.msg)
      }
      // push image
      this.imageList.push({
        uid: resp.image.id,
        name: resp.image.name,
        url: resp.image.url
      })
      // success message
      onSuccess(resp)
      console.log(resp)
    })

    return {
      abort () {
        cancel()
      }
    }
  }
}
</script>
