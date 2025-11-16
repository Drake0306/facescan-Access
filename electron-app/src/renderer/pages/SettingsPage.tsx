import { useState, useEffect } from 'react'
import MainLayout from '@/components/layout/MainLayout'
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { Label } from '@/components/ui/label'
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from '@/components/ui/select'
import { useToast } from '@/components/ui/use-toast'
import { cameraAPI } from '@/lib/api'
import { Loader2, Video, CheckCircle2, XCircle } from 'lucide-react'

interface Camera {
  index: number
  name: string
  type: string
  available: boolean
}

export default function SettingsPage() {
  const [cameras, setCameras] = useState<Camera[]>([])
  const [loading, setLoading] = useState(true)
  const [saving, setSaving] = useState(false)
  const [entryCamera, setEntryCamera] = useState<string>('')
  const [exitCamera, setExitCamera] = useState<string>('')
  const [cameraStatus, setCameraStatus] = useState<{ entry_camera: boolean; exit_camera: boolean }>({
    entry_camera: false,
    exit_camera: false,
  })
  const { toast } = useToast()

  // Fetch available cameras
  useEffect(() => {
    const fetchCameras = async () => {
      try {
        setLoading(true)
        const response = await cameraAPI.listAvailable()
        setCameras(response.data.cameras)

        // Fetch current camera status
        const statusResponse = await cameraAPI.getStatus()
        setCameraStatus(statusResponse.data)
      } catch (error) {
        toast({
          title: 'Error',
          description: 'Failed to load available cameras',
          variant: 'destructive',
        })
        console.error('Error fetching cameras:', error)
      } finally {
        setLoading(false)
      }
    }

    fetchCameras()
  }, [toast])

  const handleSave = async () => {
    try {
      setSaving(true)

      const entryIndex = entryCamera ? parseInt(entryCamera) : undefined
      const exitIndex = exitCamera ? parseInt(exitCamera) : undefined

      const response = await cameraAPI.configure(entryIndex, exitIndex)

      if (response.data.success) {
        toast({
          title: 'Success',
          description: 'Camera configuration updated successfully',
        })

        // Update camera status
        setCameraStatus({
          entry_camera: response.data.entry_camera_connected,
          exit_camera: response.data.exit_camera_connected,
        })

        // Clear selections after successful save
        setEntryCamera('')
        setExitCamera('')
      } else {
        toast({
          title: 'Warning',
          description: response.data.message || 'Some cameras failed to connect',
          variant: 'destructive',
        })
      }
    } catch (error) {
      toast({
        title: 'Error',
        description: 'Failed to update camera configuration',
        variant: 'destructive',
      })
      console.error('Error configuring cameras:', error)
    } finally {
      setSaving(false)
    }
  }

  return (
    <MainLayout>
      <div className="space-y-6">
        <div>
          <h1 className="text-3xl font-bold">Settings</h1>
          <p className="text-muted-foreground">Configure system settings and preferences</p>
        </div>

        <Card>
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <Video className="h-5 w-5" />
              Camera Configuration
            </CardTitle>
            <CardDescription>
              Select cameras for entry and exit monitoring. Available cameras are automatically detected.
            </CardDescription>
          </CardHeader>
          <CardContent className="space-y-6">
            {loading ? (
              <div className="flex items-center justify-center py-8">
                <Loader2 className="h-8 w-8 animate-spin text-muted-foreground" />
              </div>
            ) : cameras.length === 0 ? (
              <div className="text-center text-muted-foreground py-8">
                <XCircle className="h-12 w-12 mx-auto mb-3 opacity-50" />
                <p>No cameras detected. Please ensure cameras are connected.</p>
              </div>
            ) : (
              <>
                <div className="grid gap-6 md:grid-cols-2">
                  {/* Entry Camera */}
                  <div className="space-y-3">
                    <div className="flex items-center justify-between">
                      <Label htmlFor="entry-camera" className="text-base font-semibold">
                        Entry Camera
                      </Label>
                      {cameraStatus.entry_camera ? (
                        <div className="flex items-center gap-1 text-sm text-green-600">
                          <CheckCircle2 className="h-4 w-4" />
                          Connected
                        </div>
                      ) : (
                        <div className="flex items-center gap-1 text-sm text-muted-foreground">
                          <XCircle className="h-4 w-4" />
                          Not Connected
                        </div>
                      )}
                    </div>
                    <Select value={entryCamera} onValueChange={setEntryCamera}>
                      <SelectTrigger id="entry-camera">
                        <SelectValue placeholder="Select entry camera" />
                      </SelectTrigger>
                      <SelectContent>
                        {cameras.map((camera) => (
                          <SelectItem key={camera.index} value={camera.index.toString()}>
                            {camera.name} (Index {camera.index})
                          </SelectItem>
                        ))}
                      </SelectContent>
                    </Select>
                    <p className="text-sm text-muted-foreground">
                      Camera used for monitoring entry gate
                    </p>
                  </div>

                  {/* Exit Camera */}
                  <div className="space-y-3">
                    <div className="flex items-center justify-between">
                      <Label htmlFor="exit-camera" className="text-base font-semibold">
                        Exit Camera
                      </Label>
                      {cameraStatus.exit_camera ? (
                        <div className="flex items-center gap-1 text-sm text-green-600">
                          <CheckCircle2 className="h-4 w-4" />
                          Connected
                        </div>
                      ) : (
                        <div className="flex items-center gap-1 text-sm text-muted-foreground">
                          <XCircle className="h-4 w-4" />
                          Not Connected
                        </div>
                      )}
                    </div>
                    <Select value={exitCamera} onValueChange={setExitCamera}>
                      <SelectTrigger id="exit-camera">
                        <SelectValue placeholder="Select exit camera" />
                      </SelectTrigger>
                      <SelectContent>
                        {cameras.map((camera) => (
                          <SelectItem key={camera.index} value={camera.index.toString()}>
                            {camera.name} (Index {camera.index})
                          </SelectItem>
                        ))}
                      </SelectContent>
                    </Select>
                    <p className="text-sm text-muted-foreground">
                      Camera used for monitoring exit gate
                    </p>
                  </div>
                </div>

                <div className="flex items-center justify-between pt-4 border-t">
                  <p className="text-sm text-muted-foreground">
                    Found {cameras.length} available camera{cameras.length !== 1 ? 's' : ''}
                  </p>
                  <Button
                    onClick={handleSave}
                    disabled={saving || (!entryCamera && !exitCamera)}
                  >
                    {saving ? (
                      <>
                        <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                        Saving...
                      </>
                    ) : (
                      'Save Configuration'
                    )}
                  </Button>
                </div>
              </>
            )}
          </CardContent>
        </Card>
      </div>
    </MainLayout>
  )
}
