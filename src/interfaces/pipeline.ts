export interface IPipeline {
  type?: 'resource' | 'package'
  steps?: IStep[]
}

export type IStep =
  | IFieldAddStep
  | IFieldFilterStep
  | IFieldMoveStep
  | IFieldRemoveStep
  | IFieldUpdateStep

export interface IFieldAddStep {
  code: 'field-add'
  name: string
  value?: any
  formula?: string
}

export interface IFieldFilterStep {
  code: 'field-filter'
  names: string[]
}

export interface IFieldMoveStep {
  code: 'field-move'
  name: string
  position: number
}

export interface IFieldRemoveStep {
  code: 'field-remove'
  names: string[]
}

export interface IFieldUpdateStep {
  code: 'field-update'
  name: string
  value?: any
  formula?: string
  newName?: string
}
