<template><div class="home">
  <a-layout style="height:fit-content">

      <!-- header -->
      <a-layout-header>
        <a-page-header title="simple-expression-corrector" subtitle="v 1.0" :show-back="false">
        <template #extra>
            <a-avatar v-if="!isLogin" trigger-type="mask" @click="loginForm.HandleClick">
            未登录
            <template #trigger-icon>
              <IconUser/>
            </template>
            </a-avatar>
            <a-avatar v-if="isLogin" trigger-type="mask" @click="void(0)" :style="avaterStyle[Math.floor(Math.random() * avaterStyle.length)]">
            <a-image v-if="userInfo.avatar !== ''"/>
            <span v-if="userInfo.avatar === ''">
              {{ userInfo.username.substring(0, 6) }}
            </span>
            <template #trigger-icon>
              <IconBulb />
            </template>
            </a-avatar>
        </template>
        <div/>
        </a-page-header>
      </a-layout-header>

      <!-- content -->
      <a-layout-content>
        <a-upload style="padding: 20px; width:95%; text-align: left;"
          accept="image/*"
          list-type="picture"
          action="/"
          :custom-request="upload.Do"
          :file-list="upload.imageList"
        >
        <template v-slot:image="{ fileItem }">
          <a-image :src="fileItem.url" width="40" height="40"/>
          <a-button type="primary" size="mini"
            style="position:absolute; top:15px; right:100px"
            @click="res.showResult(fileItem)"
            :loading="judge.loading.get(fileItem.uid)"
          >查看结果</a-button>
        </template>
        </a-upload>
        <a-empty v-if="upload.isEmpty"/>
      </a-layout-content>

      <!-- footer -->
      <a-layout-footer>
        <!-- test -->
        <icon-to-top :size="50"/>
      </a-layout-footer>
    </a-layout>

  <!-- result -->
  <a-modal :visible="res.Visible"
  @ok="res.handleOk_bugfeedback" ok-text="反馈 Bug"
  @cancel="res.handleCancel" :hide-cancel="true"
  :closable="false"
  width="auto"
  unmountOnClose>
  <template #title>
      {{ res.Title }}
  </template>
    <div @click="() => { res.Content.preview_visible = true }">
      <a-image
      :src="res.Content.src"
      footer-position="outer"
      :preview-visible="res.Content.preview_visible"
      @preview-visible-change="() => { res.Content.preview_visible = false }"
      />
    </div>
  </a-modal>

  <!-- Bug feedback -->
  <a-drawer placeholder="right" :width="400"
    :visible="bug.Visible"
    @ok="bug.handleOk" ok-text="反馈"
    :ok-button-props="{'loading': bug.feedback_button.loading}"
    @cancel="bug.handleCancel" cancel-text="取消"
    :closable="false"
    :mask="false" :mask-closable="false"
  >
  <template #title>
      {{ bug.Title }}
  </template>
  <a-form :model="bug.Form" layout="vertical">
      <a-form-item field="email" label="邮箱">
        <a-input v-model="bug.Form.email" placeholder="please enter your email" />
      </a-form-item>
      <a-form-item field="description" label="描述">
        <a-textarea v-model="bug.Form.description" placeholder="Please enter something"
        :auto-size="{minRows: 15, maxRows: 15}"
        :max-length="500"
        show-word-limit/>
      </a-form-item>
    </a-form>
  </a-drawer>

  <!-- form -->
  <a-modal :visible="loginForm.Visible" @ok="loginForm.HandleOk" @cancel="loginForm.HandleCancle" :mask-closable="false" :hide-cancel="true" :footer="false">
    <template #title>
      simple-expression-corrector
    </template>
    <a-tabs position="left" :animation="true" :active-key="loginForm.active"  @tab-click="loginForm.SwitchTab">
      <!-- Login -->
      <a-tab-pane key="1" title="登录">
        <a-form :model="loginForm" size="large">
          <!-- username -->
          <a-form-item field="username" :label="loginForm.username.label" :help="loginForm.username.help" :extra="loginForm.username.extra" :validate-status="loginForm.username.validate_status()" feedback>
            <a-input v-model="loginForm.username.value" placeholder="Please enter your username here" />
          </a-form-item>
          <!-- password -->
          <a-form-item field="password" :label="loginForm.password.label" :help="loginForm.password.help" :extra="loginForm.password.extra" :validate-status="loginForm.password.validate_status()" feedback>
            <a-input-password v-model="loginForm.password.value" placeholder="Please enter your password here" :invisible-button="false"/>
          </a-form-item>
        </a-form>
        <a-button type="primary" shape="round" :loading="loginForm.loginButton.isLoading" :disabled="loginForm.loginButton_isDisable" @click="loginForm.loginButton.click" long>{{ loginForm.loginButton.text }}</a-button>
      </a-tab-pane>
      <!-- Register -->
      <a-tab-pane key="2" title="注册">
        <a-form :model="loginForm" size="large">
          <!-- username -->
          <a-form-item field="username" :label="loginForm.username.label" :help="loginForm.username.help" :extra="loginForm.username.extra" :validate-status="loginForm.username.validate_status()" feedback>
            <a-input v-model="loginForm.username.value" placeholder="Please enter your username here" />
          </a-form-item>
          <!-- password -->
          <a-form-item field="password" :label="loginForm.password.label" :help="loginForm.password.help" :extra="loginForm.password.extra" :validate-status="loginForm.password.validate_status()" feedback>
            <a-input-password v-model="loginForm.password.value" placeholder="Please enter your password here" :invisible-button="false"/>
          </a-form-item>
          <!-- password -->
          <a-form-item field="repasswd" :label="loginForm.repasswd.label" :help="loginForm.repasswd.help" :extra="loginForm.repasswd.extra" :validate-status="loginForm.repasswd.validate_status()" feedback>
            <a-input-password v-model="loginForm.repasswd.value" placeholder="Please repeat your password here" :invisible-button="false"/>
          </a-form-item>
        </a-form>
        <a-button type="primary" shape="round" :loading="loginForm.registerButton.isLoading" :disabled="loginForm.registerButton_isDisable" @click="loginForm.registerButton.click" long>{{ loginForm.registerButton.text }}</a-button>
      </a-tab-pane>
    </a-tabs>
  </a-modal>

</div></template>

<script lang="ts">
import { Options, Vue } from 'vue-class-component'
import { IconUser, IconBulb } from '@arco-design/web-vue/es/icon'
import axios, { AxiosResponse, Canceler } from 'axios'
import { Message, FileItem, RequestOption, UploadRequest } from '@arco-design/web-vue'
import store from '@/store'
import constantsVue from '@/components/constants.vue'

@Options({
  components: {
    IconUser,
    IconBulb
  }
})
export default class Home extends Vue {
  res = {
    Visible: false,
    Title: 'Result',
    Content: {
      src: '',
      preview_visible: false,
      onDownload: (): void => {
        console.log('TODO: Download')
      }
    },
    file: {
      id: '',
      name: '',
      url: ''
    },

    handleOk_bugfeedback: (): void => {
      this.bug.Visible = true
    },

    handleCancel: (): void => {
      this.res.Visible = false
    },
    showResult: (fileItem: {uid: string, name: string, url: string}): void => {
      this.res.file.id = fileItem.uid
      this.res.file.name = fileItem.name
      this.res.file.url = fileItem.url

      this.res.Visible = true

      const content = this.res.Content
      content.src = this.judge.imageList.get(fileItem.uid).url
      this.res.Title = fileItem.name
      content.onDownload = (): void => {
        console.log('TODO: Download')
      }
    }
  }

  bug = {
    Visible: false,
    Title: 'Bug FeedBack',
    Form: {
      email: '',
      description: ''
    },

    feedback_button: {
      loading: false
    },
    handleOk: (): void => {
      this.bug.feedback_button.loading = true
      const request = {
        upload_id: this.res.file.id,
        judge_id: this.judge.imageList.get(this.res.file.id).uid,
        email: this.bug.Form.email,
        description: this.bug.Form.description
      }
      axios.post(constantsVue.api + 'feedback/bug', request, {
        headers: {
          Authorization: 'Bearer ' + store.getters.token
        }
      }).catch((err) => {
        console.log(err)
      }).then((vhttpResp: void | AxiosResponse) => {
        // check resp is not null
        if (!vhttpResp) {
          Message.error('未知错误')
          return
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
          Message.error(httpStatus.msg)
          return
        }
        // check server status
        if (resp.status.code !== 0) {
          Message.error(resp.status.msg)
          return
        }
        Message.success('反馈成功')
      }).finally(() => {
        this.bug.feedback_button.loading = false
        this.bug.Visible = false
        this.bug.Form.email = ''
        this.bug.Form.description = ''
      })
    },

    handleCancel: (): void => {
      this.bug.Visible = false
    }

  }

  upload = {
    imageList: [] as FileItem[],
    get isEmpty ():boolean {
      return this.imageList.length === 0
    },
    Do: (option: RequestOption): UploadRequest => {
      const { onProgress, onError, onSuccess, fileItem, name } = option

      if (store.getters.token === 'null') {
        Message.info('请先登录')
        onError('Need Token')
        return {}
      }

      if ((fileItem.file as File).size >= 1024 * 1024) {
        Message.warning('图片过大, 请限制在 1 MB 以内')
        onError('Too Large Size')
        return {}
      }

      const formData = new FormData()
      formData.append(name as string || 'file', fileItem.file as Blob)

      let cancel: Canceler

      axios.post(constantsVue.api + 'upload', formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
          Authorization: 'Bearer ' + store.getters.token
        },
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
          Message.error('未知错误')
          onError('null')
          return
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
          Message.error(httpStatus.msg)
          onError(httpStatus.msg)
          return
        }
        // check server status
        if (resp.status.code !== 0) {
          Message.error(resp.status.msg)
          onError(resp.status.msg)
          return
        }
        // push image
        this.upload.imageList.push({
          uid: resp.image.id,
          name: resp.image.name,
          url: resp.image.url
        })
        // success message
        onSuccess(resp)
        Message.success('上传 ' + resp.image.name + ' 成功')
        this.judge.Do(resp.image.id)
      })

      return {
        abort () {
          cancel()
        }
      }
    }
  }

  judge = {
    imageList: new Map(),
    loading: new Map(),
    Do: (id: string): void => {
      if (store.getters.token === 'null') {
        Message.info('请先登录')
        return
      }
      this.judge.loading.set(id, true)
      const request = { id: id }
      axios.post(constantsVue.api + 'judge', request, {
        headers: {
          Authorization: 'Bearer ' + store.getters.token
        }
      }).catch((err) => {
        console.log(err)
      }).then((vhttpResp: void | AxiosResponse) => {
        // check resp is not null
        if (!vhttpResp) {
          Message.error('未知错误')
          return
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
          Message.error(httpStatus.msg)
          return
        }
        // check server status
        if (resp.status.code !== 0) {
          Message.error(resp.status.msg)
          return
        }
        // push image
        this.judge.imageList.set(id, {
          uid: resp.image.id,
          name: resp.image.name,
          url: resp.image.url
        })
        this.judge.loading.set(id, false)
      })
    }
  }

  avaterStyle = [
    { backgroundColor: '#7BC616' },
    { backgroundColor: '#14C9C9' },
    { backgroundColor: '#168CFF' },
    { backgroundColor: '#FF7D00' },
    { backgroundColor: '#FFC72E' }
  ]

  isLogin = false
  userInfo = {
    username: '',
    avatar: ''
  }

  loginForm = {
    active: '1',
    Visible: false,
    HandleClick: (): void => {
      this.loginForm.Visible = true
      this.loginForm.username.value = ''
      this.loginForm.password.value = ''
      this.loginForm.repasswd.value = ''
    },
    HandleOk: ():void => {
      this.loginForm.Visible = false
    },
    HandleCancle: ():void => {
      this.loginForm.Visible = false
    },
    SwitchTab: (key: string | number):void => {
      this.loginForm.active = key as string
      this.loginForm.username.value = ''
      this.loginForm.password.value = ''
      this.loginForm.repasswd.value = ''
    },
    username: {
      label: '用户名',
      value: '',
      status: '',
      help: '',
      extra: '5 ~ 32 个字符, 不允许包含特殊字符',
      validate_status: (): 'success' | 'warning' | 'error' | 'validating' | undefined => {
        const u = this.loginForm.username
        const reg = /[^0-9a-zA-Z]/
        if (u.value === '') {
          u.help = ''
          u.extra = '5 ~ 32 个字符, 不允许包含特殊字符'
          u.status = ''
        } else if (u.value.length < 5) {
          u.help = 'the username is too short'
          u.extra = ''
          u.status = 'warning'
        } else if (u.value.length > 32) {
          u.help = 'the username is too long'
          u.extra = ''
          u.status = 'warning'
        } else if (reg.exec(u.value) !== null) {
          u.help = '不允许包含特殊字符'
          u.extra = ''
          u.status = 'error'
        } else {
          u.help = ''
          u.extra = ''
          u.status = 'success'
        }
        if (u.status === '') {
          return undefined
        }
        return u.status as 'success' | 'warning' | 'error' | 'validating' | undefined
      }
    },
    password: {
      label: '密码',
      value: '',
      status: '',
      help: '',
      extra: '5 ~ 32 个字符, 特殊字符只允许 !@#$%^&*()',
      validate_status: (): 'success' | 'warning' | 'error' | 'validating' | undefined => {
        const p = this.loginForm.password
        const reg = /[^0-9a-zA-Z!@#$%^&*()]/
        if (p.value === '') {
          p.help = ''
          p.extra = '5 ~ 32 个字符, 特殊字符只允许 !@#$%^&*()'
          p.status = ''
        } else if (p.value.length < 5) {
          p.help = 'the password is too short'
          p.extra = ''
          p.status = 'warning'
        } else if (p.value.length > 32) {
          p.help = 'the password is too long'
          p.extra = ''
          p.status = 'warning'
        } else if (reg.exec(p.value) !== null) {
          p.help = '包含了不支持的字符'
          p.extra = ''
          p.status = 'error'
        } else {
          p.help = ''
          p.extra = ''
          p.status = 'success'
        }
        if (p.status === '') {
          return undefined
        }
        return p.status as 'success' | 'warning' | 'error' | 'validating' | undefined
      }
    },
    repasswd: {
      label: '重复密码',
      value: '',
      status: '',
      help: '',
      extra: '',
      validate_status: (): 'success' | 'warning' | 'error' | 'validating' | undefined => {
        const p = this.loginForm.password
        const r = this.loginForm.repasswd
        const reg = /[^0-9a-zA-Z!@#$%^&*()]/
        if (r.value === '') {
          r.help = ''
          r.extra = ''
          r.status = ''
        } else if (reg.exec(r.value) !== null) {
          r.help = '包含了不支持的字符'
          r.extra = ''
          r.status = 'error'
        } else if (r.value !== p.value) {
          r.help = '两次输入的密码不一致'
          r.extra = ''
          r.status = 'error'
        } else {
          r.help = ''
          r.extra = ''
          r.status = 'success'
        }
        if (r.status === '') {
          return undefined
        }
        return r.status as 'success' | 'warning' | 'error' | 'validating' | undefined
      }
    },
    loginButton: {
      isLoading: false,
      isDisable: false,
      text: '登录',
      click: ():void => {
        this.loginForm.loginButton.isLoading = true
        axios.post(constantsVue.api + 'user/login', {
          username: this.loginForm.username.value,
          password: this.loginForm.password.value
        }).then((vHttpResp: void | AxiosResponse) => {
          // check resp is not null
          if (!vHttpResp) {
            Message.error('未知错误')
            return
          }
          // parse resp
          const httpResp = vHttpResp as AxiosResponse
          const httpStatus = {
            code: httpResp.status,
            msg: httpResp.statusText
          }
          const resp = httpResp.data
          // check http status
          if (httpStatus.code !== 200) {
            Message.error(httpStatus.msg)
            return
          }
          // check server status
          if (resp.status.code !== 0) {
            Message.error(resp.status.msg)
            return
          }
          // save token to vuex
          store.commit('saveUserInfo', {
            id: resp.id,
            token: resp.token
          })
          this.isLogin = true
          this.userInfo.username = this.loginForm.username.value
          this.loginForm.Visible = false
          Message.success('登录成功')
        }).finally(() => {
          this.loginForm.loginButton.isLoading = false
          this.loginForm.username.value = ''
          this.loginForm.password.value = ''
          this.loginForm.repasswd.value = ''
        })
      }
    },
    registerButton: {
      isLoading: false,
      isDisable: false,
      text: '注册',
      click: ():void => {
        this.loginForm.registerButton.isLoading = true
        axios.post(constantsVue.api + 'user/register', {
          username: this.loginForm.username.value,
          password: this.loginForm.password.value
        }).then((vHttpResp: void | AxiosResponse) => {
          // check resp is not null
          if (!vHttpResp) {
            Message.error('未知错误')
            return
          }
          // parse resp
          const httpResp = vHttpResp as AxiosResponse
          const httpStatus = {
            code: httpResp.status,
            msg: httpResp.statusText
          }
          const resp = httpResp.data
          // check http status
          if (httpStatus.code !== 200) {
            Message.error(httpStatus.msg)
            return
          }
          // check server status
          if (resp.status.code !== 0) {
            Message.error(resp.status.msg)
            return
          }
          // save token to vuex
          store.commit('saveUserInfo', {
            id: resp.id,
            token: resp.token
          })
          this.isLogin = true
          this.userInfo.username = this.loginForm.username.value
          this.loginForm.Visible = false
          Message.success('注册成功')
        }).finally(() => {
          this.loginForm.registerButton.isLoading = false
          this.loginForm.username.value = ''
          this.loginForm.password.value = ''
          this.loginForm.repasswd.value = ''
        })
      }
    },
    get loginButton_isDisable (): boolean {
      return this.username.status !== 'success' || this.password.status !== 'success'
    },
    get registerButton_isDisable (): boolean {
      return this.username.status !== 'success' || this.password.status !== 'success' || this.repasswd.status !== 'success'
    }
  }
}

</script>

<style></style>
