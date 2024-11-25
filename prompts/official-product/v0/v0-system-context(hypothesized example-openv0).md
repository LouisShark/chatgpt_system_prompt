```json
[
  {
    "name": "Accordion",
    "description": "A vertically stacked set of interactive headings that each reveal a section of content.",
    "docs_path": "build\\gits\\shadcn-ui$ui-openv0remix\\docs\\accordion.mdx",
    "docs": {
      "import": {
        "source": "accordion.mdx",
        "code": "import {\n  Accordion,\n  AccordionContent,\n  AccordionItem,\n  AccordionTrigger,\n} from \"@/components/ui/accordion\""
      },
      "use": [
        {
          "source": "accordion.mdx",
          "code": "<Accordion type=\"single\" collapsible>\n  <AccordionItem value=\"item-1\">\n    <AccordionTrigger>Is it accessible?</AccordionTrigger>\n    <AccordionContent>\n      Yes. It adheres to the WAI-ARIA design pattern.\n    </AccordionContent>\n  </AccordionItem>\n</Accordion>"
        }
      ],
      "examples": [
        {
          "source": "accordion-demo.tsx",
          "code": "import {\r\n  Accordion,\r\n  AccordionContent,\r\n  AccordionItem,\r\n  AccordionTrigger,\r\n} from \"@/components/ui/accordion\"\r\n\r\nexport default function AccordionDemo() {\r\n  return (\r\n    <Accordion type=\"single\" collapsible className=\"w-full\">\r\n      <AccordionItem value=\"item-1\">\r\n        <AccordionTrigger>Is it accessible?</AccordionTrigger>\r\n        <AccordionContent>\r\n          Yes. It adheres to the WAI-ARIA design pattern.\r\n        </AccordionContent>\r\n      </AccordionItem>\r\n      <AccordionItem value=\"item-2\">\r\n        <AccordionTrigger>Is it styled?</AccordionTrigger>\r\n        <AccordionContent>\r\n          Yes. It comes with default styles that matches the other\r\n          components&apos; aesthetic.\r\n        </AccordionContent>\r\n      </AccordionItem>\r\n      <AccordionItem value=\"item-3\">\r\n        <AccordionTrigger>Is it animated?</AccordionTrigger>\r\n        <AccordionContent>\r\n          Yes. It&apos;s animated by default, but you can disable it if you\r\n          prefer.\r\n        </AccordionContent>\r\n      </AccordionItem>\r\n    </Accordion>\r\n  )\r\n}"
        }
      ]
    }
  },
  {
    "name": "Alert Dialog",
    "description": "A modal dialog that interrupts the user with important content and expects a response.",
    "docs_path": "build\\gits\\shadcn-ui$ui-openv0remix\\docs\\alert-dialog.mdx",
    "docs": {
      "import": {
        "source": "alert-dialog.mdx",
        "code": "import {\n  AlertDialog,\n  AlertDialogAction,\n  AlertDialogCancel,\n  AlertDialogContent,\n  AlertDialogDescription,\n  AlertDialogFooter,\n  AlertDialogHeader,\n  AlertDialogTitle,\n  AlertDialogTrigger,\n} from \"@/components/ui/alert-dialog\""
      },
      "use": [
        {
          "source": "alert-dialog.mdx",
          "code": "<AlertDialog>\n  <AlertDialogTrigger>Open</AlertDialogTrigger>\n  <AlertDialogContent>\n    <AlertDialogHeader>\n      <AlertDialogTitle>Are you absolutely sure?</AlertDialogTitle>\n      <AlertDialogDescription>\n        This action cannot be undone. This will permanently delete your account\n        and remove your data from our servers.\n      </AlertDialogDescription>\n    </AlertDialogHeader>\n    <AlertDialogFooter>\n      <AlertDialogCancel>Cancel</AlertDialogCancel>\n      <AlertDialogAction>Continue</AlertDialogAction>\n    </AlertDialogFooter>\n  </AlertDialogContent>\n</AlertDialog>"
        }
      ],
      "examples": [
        {
          "source": "alert-dialog-demo.tsx",
          "code": "import {\r\n  AlertDialog,\r\n  AlertDialogAction,\r\n  AlertDialogCancel,\r\n  AlertDialogContent,\r\n  AlertDialogDescription,\r\n  AlertDialogFooter,\r\n  AlertDialogHeader,\r\n  AlertDialogTitle,\r\n  AlertDialogTrigger,\r\n} from \"@/components/ui/alert-dialog\"\r\nimport { Button } from \"@/components/ui/button\"\r\n\r\nexport default function AlertDialogDemo() {\r\n  return (\r\n    <AlertDialog>\r\n      <AlertDialogTrigger asChild>\r\n        <Button variant=\"outline\">Show Dialog</Button>\r\n      </AlertDialogTrigger>\r\n      <AlertDialogContent>\r\n        <AlertDialogHeader>\r\n          <AlertDialogTitle>Are you absolutely sure?</AlertDialogTitle>\r\n          <AlertDialogDescription>\r\n            This action cannot be undone. This will permanently delete your\r\n            account and remove your data from our servers.\r\n          </AlertDialogDescription>\r\n        </AlertDialogHeader>\r\n        <AlertDialogFooter>\r\n          <AlertDialogCancel>Cancel</AlertDialogCancel>\r\n          <AlertDialogAction>Continue</AlertDialogAction>\r\n        </AlertDialogFooter>\r\n      </AlertDialogContent>\r\n    </AlertDialog>\r\n  )\r\n}"
        }
      ]
    }
  },
  {
    "name": "Alert",
    "description": "Displays a callout for user attention.",
    "docs_path": "build\\gits\\shadcn-ui$ui-openv0remix\\docs\\alert.mdx",
    "docs": {
      "import": {
        "source": "alert.mdx",
        "code": "import { Alert, AlertDescription, AlertTitle } from \"@/components/ui/alert\""
      },
      "use": [
        {
          "source": "alert.mdx",
          "code": "<Alert>\n  <Terminal className=\"h-4 w-4\" />\n  <AlertTitle>Heads up!</AlertTitle>\n  <AlertDescription>\n    You can add components and dependencies to your app using the cli.\n  </AlertDescription>\n</Alert>"
        }
      ],
      "examples": [
        {
          "source": "alert-demo.tsx",
          "code": "import { Terminal, Waves } from \"lucide-react\"\r\n\r\nimport {\r\n  Alert,\r\n  AlertDescription,\r\n  AlertTitle,\r\n} from \"@/components/ui/alert\"\r\n\r\nexport default function AlertDemo() {\r\n  return (\r\n    <Alert>\r\n      <Terminal className=\"h-4 w-4\" />\r\n      <AlertTitle>Heads up!</AlertTitle>\r\n      <AlertDescription>\r\n        You can add components to your app using the cli.\r\n      </AlertDescription>\r\n    </Alert>\r\n  )\r\n}"
        },
        {
          "source": "alert-destructive.tsx",
          "code": "import { AlertCircle, FileWarning, Terminal } from \"lucide-react\"\r\n\r\nimport {\r\n  Alert,\r\n  AlertDescription,\r\n  AlertTitle,\r\n} from \"@/components/ui/alert\"\r\n\r\nexport default function AlertDestructive() {\r\n  return (\r\n    <Alert variant=\"destructive\">\r\n      <AlertCircle className=\"h-4 w-4\" />\r\n      <AlertTitle>Error</AlertTitle>\r\n      <AlertDescription>\r\n        Your session has expired. Please log in again.\r\n      </AlertDescription>\r\n    </Alert>\r\n  )\r\n}"
        },
        {
          "source": "alert-dialog-demo.tsx",
          "code": "import {\r\n  AlertDialog,\r\n  AlertDialogAction,\r\n  AlertDialogCancel,\r\n  AlertDialogContent,\r\n  AlertDialogDescription,\r\n  AlertDialogFooter,\r\n  AlertDialogHeader,\r\n  AlertDialogTitle,\r\n  AlertDialogTrigger,\r\n} from \"@/components/ui/alert-dialog\"\r\nimport { Button } from \"@/components/ui/button\"\r\n\r\nexport default function AlertDialogDemo() {\r\n  return (\r\n    <AlertDialog>\r\n      <AlertDialogTrigger asChild>\r\n        <Button variant=\"outline\">Show Dialog</Button>\r\n      </AlertDialogTrigger>\r\n      <AlertDialogContent>\r\n        <AlertDialogHeader>\r\n          <AlertDialogTitle>Are you absolutely sure?</AlertDialogTitle>\r\n          <AlertDialogDescription>\r\n            This action cannot be undone. This will permanently delete your\r\n            account and remove your data from our servers.\r\n          </AlertDialogDescription>\r\n        </AlertDialogHeader>\r\n        <AlertDialogFooter>\r\n          <AlertDialogCancel>Cancel</AlertDialogCancel>\r\n          <AlertDialogAction>Continue</AlertDialogAction>\r\n        </AlertDialogFooter>\r\n      </AlertDialogContent>\r\n    </AlertDialog>\r\n  )\r\n}"
        }
      ]
    }
  },
  {
    "name": "Aspect Ratio",
    "description": "Displays content within a desired ratio.",
    "docs_path": "build\\gits\\shadcn-ui$ui-openv0remix\\docs\\aspect-ratio.mdx",
    "docs": {
      "import": {
        "source": "aspect-ratio.mdx",
        "code": "import { AspectRatio } from \"@/components/ui/aspect-ratio\""
      },
      "use": [
        {
          "source": "aspect-ratio.mdx",
          "code": "<div className=\"w-[450px]\">\n  <AspectRatio ratio={16 / 9}>\n    <img src=\"...\" alt=\"Image\" className=\"rounded-md object-cover\" />\n  </AspectRatio>\n</div>"
        }
      ],
      "examples": [
        {
          "source": "aspect-ratio-demo.tsx",
          "code": "import Image from \"next/image\"\r\n\r\nimport { AspectRatio } from \"@/components/ui/aspect-ratio\"\r\n\r\nexport default function AspectRatioDemo() {\r\n  return (\r\n    <AspectRatio ratio={16 / 9} className=\"bg-muted\">\r\n      <Image\r\n        src=\"https://images.unsplash.com/photo-1588345921523-c2dcdb7f1dcd?w=800&dpr=2&q=80\"\r\n        alt=\"Photo by Drew Beamer\"\r\n        fill\r\n        className=\"rounded-md object-cover\"\r\n      />\r\n    </AspectRatio>\r\n  )\r\n}"
        }
      ]
    }
  },
  {
    "name": "Avatar",
    "description": "An image element with a fallback for representing the user.",
    "docs_path": "build\\gits\\shadcn-ui$ui-openv0remix\\docs\\avatar.mdx",
    "docs": {
      "import": {
        "source": "avatar.mdx",
        "code": "import { Avatar, AvatarFallback, AvatarImage } from \"@/components/ui/avatar\""
      },
      "use": [
        {
          "source": "avatar.mdx",
          "code": "<Avatar>\n  <AvatarImage src=\"https://github.com/shadcn.png\" />\n  <AvatarFallback>CN</AvatarFallback>\n</Avatar>"
        }
      ],
      "examples": [
        {
          "source": "avatar-demo.tsx",
          "code": "import {\r\n  Avatar,\r\n  AvatarFallback,\r\n  AvatarImage,\r\n} from \"@/components/ui/avatar\"\r\n\r\nexport default function AvatarDemo() {\r\n  return (\r\n    <Avatar>\r\n      <AvatarImage src=\"https://github.com/shadcn.png\" alt=\"@shadcn\" />\r\n      <AvatarFallback>CN</AvatarFallback>\r\n    </Avatar>\r\n  )\r\n}"
        }
      ]
    }
  },
  {
    "name": "Badge",
    "description": "Displays a badge or a component that looks like a badge.",
    "docs_path": "build\\gits\\shadcn-ui$ui-openv0remix\\docs\\badge.mdx",
    "docs": {
      "import": {
        "source": "badge.mdx",
        "code": "import { Badge } from \"@/components/ui/badge\""
      },
      "use": [
        {
          "source": "badge.mdx",
          "code": "<Badge variant=\"outline\">Badge</Badge>"
        },
        {
          "source": "badge.mdx",
          "code": "import { badgeVariants } from \"@/components/ui/badge\"\n<Link className={badgeVariants({ variant: \"outline\" })}>Badge</Link>"
        }
      ],
      "examples": [
        {
          "source": "badge-demo.tsx",
          "code": "import { Badge } from \"@/components/ui/badge\"\r\n\r\nexport default function BadgeDemo() {\r\n  return <Badge>Badge</Badge>\r\n}"
        },
        {
          "source": "badge-destructive.tsx",
          "code": "import { Badge } from \"@/components/ui/badge\"\r\n\r\nexport default function BadgeDestructive() {\r\n  return <Badge variant=\"destructive\">Destructive</Badge>\r\n}"
        },
        {
          "source": "badge-outline.tsx",
          "code": "import { Badge } from \"@/components/ui/badge\"\r\n\r\nexport default function BadgeOutline() {\r\n  return <Badge variant=\"outline\">Outline</Badge>\r\n}"
        },
        {
          "source": "badge-secondary.tsx",
          "code": "import { Badge } from \"@/components/ui/badge\"\r\n\r\nexport default function BadgeSecondary() {\r\n  return <Badge variant=\"secondary\">Secondary</Badge>\r\n}"
        }
      ]
    }
  },
  {
    "name": "Button",
    "description": "Displays a button or a component that looks like a button.",
    "docs_path": "build\\gits\\shadcn-ui$ui-openv0remix\\docs\\button.mdx",
    "docs": {
      "import": {
        "source": "button.mdx",
        "code": "import { Button } from \"@/components/ui/button\""
      },
      "use": [
        {
          "source": "button.mdx",
          "code": "<Button variant=\"outline\">Button</Button>"
        },
        {
          "source": "button.mdx",
          "code": "import { buttonVariants } from \"@/components/ui/button\"\n<Link className={buttonVariants({ variant: \"outline\" })}>Click here</Link>"
        }
      ],
      "examples": [
        {
          "source": "button-as-child.tsx",
          "code": "import Link from \"next/link\"\r\n\r\nimport { Button } from \"@/components/ui/button\"\r\n\r\nexport default function ButtonAsChild() {\r\n  return (\r\n    <Button asChild>\r\n      <Link href=\"/login\">Login</Link>\r\n    </Button>\r\n  )\r\n}"
        },
        {
          "source": "button-demo.tsx",
          "code": "import { Button } from \"@/components/ui/button\"\r\n\r\nexport default function ButtonDemo() {\r\n  return <Button>Button</Button>\r\n}"
        },
        {
          "source": "button-destructive.tsx",
          "code": "import { Button } from \"@/components/ui/button\"\r\n\r\nexport default function ButtonDestructive() {\r\n  return <Button variant=\"destructive\">Destructive</Button>\r\n}"
        },
        {
          "source": "button-ghost.tsx",
          "code": "import { Button } from \"@/components/ui/button\"\r\n\r\nexport default function ButtonGhost() {\r\n  return <Button variant=\"ghost\">Ghost</Button>\r\n}"
        },
        {
          "source": "button-icon.tsx",
          "code": "import { ChevronRight } from \"lucide-react\"\r\n\r\nimport { Button } from \"@/components/ui/button\"\r\n\r\nexport default function ButtonIcon() {\r\n  return (\r\n    <Button variant=\"outline\" size=\"icon\">\r\n      <ChevronRight className=\"h-4 w-4\" />\r\n    </Button>\r\n  )\r\n}"
        },
        {
          "source": "button-link.tsx",
          "code": "import { Button } from \"@/components/ui/button\"\r\n\r\nexport default function ButtonLink() {\r\n  return <Button variant=\"link\">Link</Button>\r\n}"
        },
        {
          "source": "button-loading.tsx",
          "code": "import { Loader2 } from \"lucide-react\"\r\n\r\nimport { Button } from \"@/components/ui/button\"\r\n\r\nexport default function ButtonLoading() {\r\n  return (\r\n    <Button disabled>\r\n      <Loader2 className=\"mr-2 h-4 w-4 animate-spin\" />\r\n      Please wait\r\n    </Button>\r\n  )\r\n}"
        },
        {
          "source": "button-outline.tsx",
          "code": "import { Button } from \"@/components/ui/button\"\r\n\r\nexport default function ButtonOutline() {\r\n  return <Button variant=\"outline\">Outline</Button>\r\n}"
        },
        {
          "source": "button-secondary.tsx",
          "code": "import { Button } from \"@/components/ui/button\"\r\n\r\nexport default function ButtonSecondary() {\r\n  return <Button variant=\"secondary\">Secondary</Button>\r\n}"
        },
        {
          "source": "button-with-icon.tsx",
          "code": "import { Mail } from \"lucide-react\"\r\n\r\nimport { Button } from \"@/components/ui/button\"\r\n\r\nexport default function ButtonWithIcon() {\r\n  return (\r\n    <Button>\r\n      <Mail className=\"mr-2 h-4 w-4\" /> Login with Email\r\n    </Button>\r\n  )\r\n}"
        }
      ]
    }
  },
  {
    "name": "Calendar",
    "description": "A date field component that allows users to enter and edit date.",
    "docs_path": "build\\gits\\shadcn-ui$ui-openv0remix\\docs\\calendar.mdx",
    "docs": {
      "import": {
        "source": "calendar.mdx",
        "code": "import { Calendar } from \"@/components/ui/calendar\""
      },
      "use": [
        {
          "source": "calendar.mdx",
          "code": "<Calendar\n  mode=\"single\"\n  selected={date}\n  onSelect={setDate}\n  className=\"rounded-md border\"\n/>"
        }
      ],
      "examples": [
        {
          "source": "calendar-demo.tsx",
          "code": "\"use client\"\r\n\r\nimport * as React from \"react\"\r\n\r\nimport { Calendar } from \"@/components/ui/calendar\"\r\n\r\nexport default function CalendarDemo() {\r\n  const [date, setDate] = React.useState<Date | undefined>(new Date())\r\n\r\n  return (\r\n    <Calendar\r\n      mode=\"single\"\r\n      selected={date}\r\n      onSelect={setDate}\r\n      className=\"rounded-md border\"\r\n    />\r\n  )\r\n}"
        }
      ]
    }
  },
  {
    "name": "Card",
    "description": "Displays a card with header, content, and footer.",
    "docs_path": "build\\gits\\shadcn-ui$ui-openv0remix\\docs\\card.mdx",
    "docs": {
      "import": {
        "source": "card.mdx",
        "code": "import {\n  Card,\n  CardContent,\n  CardDescription,\n  CardFooter,\n  CardHeader,\n  CardTitle,\n} from \"@/components/ui/card\""
      },
      "use": [
        {
          "source": "card.mdx",
          "code": "<Card>\n  <CardHeader>\n    <CardTitle>Card Title</CardTitle>\n    <CardDescription>Card Description</CardDescription>\n  </CardHeader>\n  <CardContent>\n    <p>Card Content</p>\n  </CardContent>\n  <CardFooter>\n    <p>Card Footer</p>\n  </CardFooter>\n</Card>"
        }
      ],
      "examples": [
        {
          "source": "card-demo.tsx",
          "code": "import { BellRing, Check } from \"lucide-react\"\r\n\r\nimport { cn } from \"@/lib/utils\"\r\nimport { Button } from \"@/components/ui/button\"\r\nimport {\r\n  Card,\r\n  CardContent,\r\n  CardDescription,\r\n  CardFooter,\r\n  CardHeader,\r\n  CardTitle,\r\n} from \"@/components/ui/card\"\r\nimport { Separator } from \"@/components/ui/separator\"\r\nimport { Switch } from \"@/components/ui/switch\"\r\n\r\nconst notifications = [\r\n  {\r\n    title: \"Your call has been confirmed.\",\r\n    description: \"1 hour ago\",\r\n  },\r\n  {\r\n    title: \"You have a new message!\",\r\n    description: \"1 hour ago\",\r\n  },\r\n  {\r\n    title: \"Your subscription is expiring soon!\",\r\n    description: \"2 hours ago\",\r\n  },\r\n]\r\n\r\ntype CardProps = React.ComponentProps<typeof Card>\r\n\r\nexport default function CardDemo({ className, ...props }: CardProps) {\r\n  return (\r\n    <Card className={cn(\"w-[380px]\", className)} {...props}>\r\n      <CardHeader>\r\n        <CardTitle>Notifications</CardTitle>\r\n        <CardDescription>You have 3 unread messages.</CardDescription>\r\n      </CardHeader>\r\n      <CardContent className=\"grid gap-4\">\r\n        <div className=\" flex items-center space-x-4 rounded-md border p-4\">\r\n          <BellRing />\r\n          <div className=\"flex-1 space-y-1\">\r\n            <p className=\"text-sm font-medium leading-none\">\r\n              Push Notifications\r\n            </p>\r\n            <p className=\"text-sm text-muted-foreground\">\r\n              Send notifications to device.\r\n            </p>\r\n          </div>\r\n          <Switch />\r\n        </div>\r\n        <div>\r\n          {notifications.map((notification, index) => (\r\n            <div\r\n              key={index}\r\n              className=\"mb-4 grid grid-cols-[25px_1fr] items-start pb-4 last:mb-0 last:pb-0\"\r\n            >\r\n              <span className=\"flex h-2 w-2 translate-y-1 rounded-full bg-sky-500\" />\r\n              <div className=\"space-y-1\">\r\n                <p className=\"text-sm font-medium leading-none\">\r\n                  {notification.title}\r\n                </p>\r\n                <p className=\"text-sm text-muted-foreground\">\r\n                  {notification.description}\r\n                </p>\r\n              </div>\r\n            </div>\r\n          ))}\r\n        </div>\r\n      </CardContent>\r\n      <CardFooter>\r\n        <Button className=\"w-full\">\r\n          <Check className=\"mr-2 h-4 w-4\" /> Mark all as read\r\n        </Button>\r\n      </CardFooter>\r\n    </Card>\r\n  )\r\n}"
        },
        {
          "source": "card-with-form.tsx",
          "code": "import * as React from \"react\"\r\n\r\nimport { Button } from \"@/components/ui/button\"\r\nimport {\r\n  Card,\r\n  CardContent,\r\n  CardDescription,\r\n  CardFooter,\r\n  CardHeader,\r\n  CardTitle,\r\n} from \"@/components/ui/card\"\r\nimport { Input } from \"@/components/ui/input\"\r\nimport { Label } from \"@/components/ui/label\"\r\nimport {\r\n  Select,\r\n  SelectContent,\r\n  SelectItem,\r\n  SelectTrigger,\r\n  SelectValue,\r\n} from \"@/components/ui/select\"\r\n\r\nexport default function CardWithForm() {\r\n  return (\r\n    <Card className=\"w-[350px]\">\r\n      <CardHeader>\r\n        <CardTitle>Create project</CardTitle>\r\n        <CardDescription>Deploy your new project in one-click.</CardDescription>\r\n      </CardHeader>\r\n      <CardContent>\r\n        <form>\r\n          <div className=\"grid w-full items-center gap-4\">\r\n            <div className=\"flex flex-col space-y-1.5\">\r\n              <Label htmlFor=\"name\">Name</Label>\r\n              <Input id=\"name\" placeholder=\"Name of your project\" />\r\n            </div>\r\n            <div className=\"flex flex-col space-y-1.5\">\r\n              <Label htmlFor=\"framework\">Framework</Label>\r\n              <Select>\r\n                <SelectTrigger id=\"framework\">\r\n                  <SelectValue placeholder=\"Select\" />\r\n                </SelectTrigger>\r\n                <SelectContent position=\"popper\">\r\n                  <SelectItem value=\"next\">Next.js</SelectItem>\r\n                  <SelectItem value=\"sveltekit\">SvelteKit</SelectItem>\r\n                  <SelectItem value=\"astro\">Astro</SelectItem>\r\n                  <SelectItem value=\"nuxt\">Nuxt.js</SelectItem>\r\n                </SelectContent>\r\n              </Select>\r\n            </div>\r\n          </div>\r\n        </form>\r\n      </CardContent>\r\n      <CardFooter className=\"flex justify-between\">\r\n        <Button variant=\"outline\">Cancel</Button>\r\n        <Button>Deploy</Button>\r\n      </CardFooter>\r\n    </Card>\r\n  )\r\n}"
        }
      ]
    }
  },
  {
    "name": "Checkbox",
    "description": "A control that allows the user to toggle between checked and not checked.",
    "docs_path": "build\\gits\\shadcn-ui$ui-openv0remix\\docs\\checkbox.mdx",
    "docs": {
      "import": {
        "source": "checkbox.mdx",
        "code": "import { Checkbox } from \"@/components/ui/checkbox\""
      },
      "use": [{ "source": "checkbox.mdx", "code": "<Checkbox />" }],
      "examples": [
        {
          "source": "checkbox-demo.tsx",
          "code": "\"use client\"\r\n\r\nimport { Checkbox } from \"@/components/ui/checkbox\"\r\n\r\nexport default function CheckboxDemo() {\r\n  return (\r\n    <div className=\"flex items-center space-x-2\">\r\n      <Checkbox id=\"terms\" />\r\n      <label\r\n        htmlFor=\"terms\"\r\n        className=\"text-sm font-medium leading-none peer-disabled:cursor-not-allowed peer-disabled:opacity-70\"\r\n      >\r\n        Accept terms and conditions\r\n      </label>\r\n    </div>\r\n  )\r\n}"
        },
        {
          "source": "checkbox-disabled.tsx",
          "code": "import { Checkbox } from \"@/components/ui/checkbox\"\r\n\r\nexport default function CheckboxDisabled() {\r\n  return (\r\n    <div className=\"flex items-center space-x-2\">\r\n      <Checkbox id=\"terms2\" disabled />\r\n      <label\r\n        htmlFor=\"terms2\"\r\n        className=\"text-sm font-medium leading-none peer-disabled:cursor-not-allowed peer-disabled:opacity-70\"\r\n      >\r\n        Accept terms and conditions\r\n      </label>\r\n    </div>\r\n  )\r\n}"
        },
        {
          "source": "checkbox-with-text.tsx",
          "code": "\"use client\"\r\n\r\nimport { Checkbox } from \"@/components/ui/checkbox\"\r\n\r\nexport default function CheckboxWithText() {\r\n  return (\r\n    <div className=\"items-top flex space-x-2\">\r\n      <Checkbox id=\"terms1\" />\r\n      <div className=\"grid gap-1.5 leading-none\">\r\n        <label\r\n          htmlFor=\"terms1\"\r\n          className=\"text-sm font-medium leading-none peer-disabled:cursor-not-allowed peer-disabled:opacity-70\"\r\n        >\r\n          Accept terms and conditions\r\n        </label>\r\n        <p className=\"text-sm text-muted-foreground\">\r\n          You agree to our Terms of Service and Privacy Policy.\r\n        </p>\r\n      </div>\r\n    </div>\r\n  )\r\n}"
        }
      ]
    }
  },
  {
    "name": "Collapsible",
    "description": "An interactive component which expands/collapses a panel.",
    "docs_path": "build\\gits\\shadcn-ui$ui-openv0remix\\docs\\collapsible.mdx",
    "docs": {
      "import": {
        "source": "collapsible.mdx",
        "code": "import {\n  Collapsible,\n  CollapsibleContent,\n  CollapsibleTrigger,\n} from \"@/components/ui/collapsible\""
      },
      "use": [
        {
          "source": "collapsible.mdx",
          "code": "<Collapsible>\n  <CollapsibleTrigger>Can I use this in my project?</CollapsibleTrigger>\n  <CollapsibleContent>\n    Yes. Free to use for personal and commercial projects. No attribution\n    required.\n  </CollapsibleContent>\n</Collapsible>"
        }
      ],
      "examples": [
        {
          "source": "collapsible-demo.tsx",
          "code": "\"use client\"\r\n\r\nimport * as React from \"react\"\r\nimport { ChevronsUpDown, Plus, X } from \"lucide-react\"\r\n\r\nimport { Button } from \"@/components/ui/button\"\r\nimport {\r\n  Collapsible,\r\n  CollapsibleContent,\r\n  CollapsibleTrigger,\r\n} from \"@/components/ui/collapsible\"\r\n\r\nexport default function CollapsibleDemo() {\r\n  const [isOpen, setIsOpen] = React.useState(false)\r\n\r\n  return (\r\n    <Collapsible\r\n      open={isOpen}\r\n      onOpenChange={setIsOpen}\r\n      className=\"w-[350px] space-y-2\"\r\n    >\r\n      <div className=\"flex items-center justify-between space-x-4 px-4\">\r\n        <h4 className=\"text-sm font-semibold\">\r\n          @peduarte starred 3 repositories\r\n        </h4>\r\n        <CollapsibleTrigger asChild>\r\n          <Button variant=\"ghost\" size=\"sm\" className=\"w-9 p-0\">\r\n            <ChevronsUpDown className=\"h-4 w-4\" />\r\n            <span className=\"sr-only\">Toggle</span>\r\n          </Button>\r\n        </CollapsibleTrigger>\r\n      </div>\r\n      <div className=\"rounded-md border px-4 py-3 font-mono text-sm\">\r\n        @radix-ui/primitives\r\n      </div>\r\n      <CollapsibleContent className=\"space-y-2\">\r\n        <div className=\"rounded-md border px-4 py-3 font-mono text-sm\">\r\n          @radix-ui/colors\r\n        </div>\r\n        <div className=\"rounded-md border px-4 py-3 font-mono text-sm\">\r\n          @stitches/react\r\n        </div>\r\n      </CollapsibleContent>\r\n    </Collapsible>\r\n  )\r\n}"
        }
      ]
    }
  },
  {
    "name": "Combobox",
    "description": "Autocomplete input and command palette with a list of suggestions.",
    "docs_path": "build\\gits\\shadcn-ui$ui-openv0remix\\docs\\combobox.mdx",
    "docs": {
      "import": {
        "source": "combobox.mdx",
        "code": "\"use client\"\n\nimport * as React from \"react\"\nimport { Check, ChevronsUpDown } from \"lucide-react\"\n\nimport { cn } from \"@/lib/utils\"\nimport { Button } from \"@/components/ui/button\"\nimport {\n  Command,\n  CommandEmpty,\n  CommandGroup,\n  CommandInput,\n  CommandItem,\n} from \"@/components/ui/command\"\nimport {\n  Popover,\n  PopoverContent,\n  PopoverTrigger,\n} from \"@/components/ui/popover\"\n\nconst frameworks = [\n  {\n    value: \"next.js\",\n    label: \"Next.js\",\n  },\n  {\n    value: \"sveltekit\",\n    label: \"SvelteKit\",\n  },\n  {\n    value: \"nuxt.js\",\n    label: \"Nuxt.js\",\n  },\n  {\n    value: \"remix\",\n    label: \"Remix\",\n  },\n  {\n    value: \"astro\",\n    label: \"Astro\",\n  },\n]\n\nexport function ComboboxDemo() {\n  const [open, setOpen] = React.useState(false)\n  const [value, setValue] = React.useState(\"\")\n\n  return (\n    <Popover open={open} onOpenChange={setOpen}>\n      <PopoverTrigger asChild>\n        <Button\n          variant=\"outline\"\n          role=\"combobox\"\n          aria-expanded={open}\n          className=\"w-[200px] justify-between\"\n        >\n          {value\n            ? frameworks.find((framework) => framework.value === value)?.label\n            : \"Select framework...\"}\n          <ChevronsUpDown className=\"ml-2 h-4 w-4 shrink-0 opacity-50\" />\n        </Button>\n      </PopoverTrigger>\n      <PopoverContent className=\"w-[200px] p-0\">\n        <Command>\n          <CommandInput placeholder=\"Search framework...\" />\n          <CommandEmpty>No framework found.</CommandEmpty>\n          <CommandGroup>\n            {frameworks.map((framework) => (\n              <CommandItem\n                key={framework.value}\n                onSelect={(currentValue) => {\n                  setValue(currentValue === value ? \"\" : currentValue)\n                  setOpen(false)\n                }}\n              >\n                <Check\n                  className={cn(\n                    \"mr-2 h-4 w-4\",\n                    value === framework.value ? \"opacity-100\" : \"opacity-0\"\n                  )}\n                />\n                {framework.label}\n              </CommandItem>\n            ))}\n          </CommandGroup>\n        </Command>\n      </PopoverContent>\n    </Popover>\n  )\n}"
      },
      "use": [],
      "examples": [
        {
          "source": "combobox-demo.tsx",
          "code": "\"use client\"\r\n\r\nimport * as React from \"react\"\r\nimport { Check, ChevronsUpDown } from \"lucide-react\"\r\n\r\nimport { cn } from \"@/lib/utils\"\r\nimport { Button } from \"@/components/ui/button\"\r\nimport {\r\n  Command,\r\n  CommandEmpty,\r\n  CommandGroup,\r\n  CommandInput,\r\n  CommandItem,\r\n} from \"@/components/ui/command\"\r\nimport {\r\n  Popover,\r\n  PopoverContent,\r\n  PopoverTrigger,\r\n} from \"@/components/ui/popover\"\r\n\r\nconst frameworks = [\r\n  {\r\n    value: \"next.js\",\r\n    label: \"Next.js\",\r\n  },\r\n  {\r\n    value: \"sveltekit\",\r\n    label: \"SvelteKit\",\r\n  },\r\n  {\r\n    value: \"nuxt.js\",\r\n    label: \"Nuxt.js\",\r\n  },\r\n  {\r\n    value: \"remix\",\r\n    label: \"Remix\",\r\n  },\r\n  {\r\n    value: \"astro\",\r\n    label: \"Astro\",\r\n  },\r\n]\r\n\r\nexport default function ComboboxDemo() {\r\n  const [open, setOpen] = React.useState(false)\r\n  const [value, setValue] = React.useState(\"\")\r\n\r\n  return (\r\n    <Popover open={open} onOpenChange={setOpen}>\r\n      <PopoverTrigger asChild>\r\n        <Button\r\n          variant=\"outline\"\r\n          role=\"combobox\"\r\n          aria-expanded={open}\r\n          className=\"w-[200px] justify-between\"\r\n        >\r\n          {value\r\n            ? frameworks.find((framework) => framework.value === value)?.label\r\n            : \"Select framework...\"}\r\n          <ChevronsUpDown className=\"ml-2 h-4 w-4 shrink-0 opacity-50\" />\r\n        </Button>\r\n      </PopoverTrigger>\r\n      <PopoverContent className=\"w-[200px] p-0\">\r\n        <Command>\r\n          <CommandInput placeholder=\"Search framework...\" />\r\n          <CommandEmpty>No framework found.</CommandEmpty>\r\n          <CommandGroup>\r\n            {frameworks.map((framework) => (\r\n              <CommandItem\r\n                key={framework.value}\r\n                onSelect={(currentValue) => {\r\n                  setValue(currentValue === value ? \"\" : currentValue)\r\n                  setOpen(false)\r\n                }}\r\n              >\r\n                <Check\r\n                  className={cn(\r\n                    \"mr-2 h-4 w-4\",\r\n                    value === framework.value ? \"opacity-100\" : \"opacity-0\"\r\n                  )}\r\n                />\r\n                {framework.label}\r\n              </CommandItem>\r\n            ))}\r\n          </CommandGroup>\r\n        </Command>\r\n      </PopoverContent>\r\n    </Popover>\r\n  )\r\n}"
        },
        {
          "source": "combobox-dropdown-menu.tsx",
          "code": "\"use client\"\r\n\r\nimport * as React from \"react\"\r\nimport { Calendar, MoreHorizontal, Tags, Trash, User } from \"lucide-react\"\r\n\r\nimport { Button } from \"@/components/ui/button\"\r\nimport {\r\n  Command,\r\n  CommandEmpty,\r\n  CommandGroup,\r\n  CommandInput,\r\n  CommandItem,\r\n  CommandList,\r\n} from \"@/components/ui/command\"\r\nimport {\r\n  DropdownMenu,\r\n  DropdownMenuContent,\r\n  DropdownMenuGroup,\r\n  DropdownMenuItem,\r\n  DropdownMenuLabel,\r\n  DropdownMenuSeparator,\r\n  DropdownMenuShortcut,\r\n  DropdownMenuSub,\r\n  DropdownMenuSubContent,\r\n  DropdownMenuSubTrigger,\r\n  DropdownMenuTrigger,\r\n} from \"@/components/ui/dropdown-menu\"\r\n\r\nconst labels = [\r\n  \"feature\",\r\n  \"bug\",\r\n  \"enhancement\",\r\n  \"documentation\",\r\n  \"design\",\r\n  \"question\",\r\n  \"maintenance\",\r\n]\r\n\r\nexport default function ComboboxDropdownMenu() {\r\n  const [label, setLabel] = React.useState(\"feature\")\r\n  const [open, setOpen] = React.useState(false)\r\n\r\n  return (\r\n    <div className=\"flex w-full flex-col items-start justify-between rounded-md border px-4 py-3 sm:flex-row sm:items-center\">\r\n      <p className=\"text-sm font-medium leading-none\">\r\n        <span className=\"mr-2 rounded-lg bg-primary px-2 py-1 text-xs text-primary-foreground\">\r\n          {label}\r\n        </span>\r\n        <span className=\"text-muted-foreground\">Create a new project</span>\r\n      </p>\r\n      <DropdownMenu open={open} onOpenChange={setOpen}>\r\n        <DropdownMenuTrigger asChild>\r\n          <Button variant=\"ghost\" size=\"sm\">\r\n            <MoreHorizontal />\r\n          </Button>\r\n        </DropdownMenuTrigger>\r\n        <DropdownMenuContent align=\"end\" className=\"w-[200px]\">\r\n          <DropdownMenuLabel>Actions</DropdownMenuLabel>\r\n          <DropdownMenuGroup>\r\n            <DropdownMenuItem>\r\n              <User className=\"mr-2 h-4 w-4\" />\r\n              Assign to...\r\n            </DropdownMenuItem>\r\n            <DropdownMenuItem>\r\n              <Calendar className=\"mr-2 h-4 w-4\" />\r\n              Set due date...\r\n            </DropdownMenuItem>\r\n            <DropdownMenuSeparator />\r\n            <DropdownMenuSub>\r\n              <DropdownMenuSubTrigger>\r\n                <Tags className=\"mr-2 h-4 w-4\" />\r\n                Apply label\r\n              </DropdownMenuSubTrigger>\r\n              <DropdownMenuSubContent className=\"p-0\">\r\n                <Command>\r\n                  <CommandInput\r\n                    placeholder=\"Filter label...\"\r\n                    autoFocus={true}\r\n                  />\r\n                  <CommandList>\r\n                    <CommandEmpty>No label found.</CommandEmpty>\r\n                    <CommandGroup>\r\n                      {labels.map((label) => (\r\n                        <CommandItem\r\n                          key={label}\r\n                          onSelect={(value) => {\r\n                            setLabel(value)\r\n                            setOpen(false)\r\n                          }}\r\n                        >\r\n                          {label}\r\n                        </CommandItem>\r\n                      ))}\r\n                    </CommandGroup>\r\n                  </CommandList>\r\n                </Command>\r\n              </DropdownMenuSubContent>\r\n            </DropdownMenuSub>\r\n            <DropdownMenuSeparator />\r\n            <DropdownMenuItem className=\"text-red-600\">\r\n              <Trash className=\"mr-2 h-4 w-4\" />\r\n              Delete\r\n              <DropdownMenuShortcut>⌘⌫</DropdownMenuShortcut>\r\n            </DropdownMenuItem>\r\n          </DropdownMenuGroup>\r\n        </DropdownMenuContent>\r\n      </DropdownMenu>\r\n    </div>\r\n  )\r\n}"
        },
        {
          "source": "combobox-popover.tsx",
          "code": "\"use client\"\r\n\r\nimport * as React from \"react\"\r\nimport {\r\n  ArrowUpCircle,\r\n  CheckCircle2,\r\n  Circle,\r\n  HelpCircle,\r\n  LucideIcon,\r\n  XCircle,\r\n} from \"lucide-react\"\r\n\r\nimport { cn } from \"@/lib/utils\"\r\nimport { Button } from \"@/components/ui/button\"\r\nimport {\r\n  Command,\r\n  CommandEmpty,\r\n  CommandGroup,\r\n  CommandInput,\r\n  CommandItem,\r\n  CommandList,\r\n} from \"@/components/ui/command\"\r\nimport {\r\n  Popover,\r\n  PopoverContent,\r\n  PopoverTrigger,\r\n} from \"@/components/ui/popover\"\r\n\r\ntype Status = {\r\n  value: string\r\n  label: string\r\n  icon: LucideIcon\r\n}\r\n\r\nconst statuses: Status[] = [\r\n  {\r\n    value: \"backlog\",\r\n    label: \"Backlog\",\r\n    icon: HelpCircle,\r\n  },\r\n  {\r\n    value: \"todo\",\r\n    label: \"Todo\",\r\n    icon: Circle,\r\n  },\r\n  {\r\n    value: \"in progress\",\r\n    label: \"In Progress\",\r\n    icon: ArrowUpCircle,\r\n  },\r\n  {\r\n    value: \"done\",\r\n    label: \"Done\",\r\n    icon: CheckCircle2,\r\n  },\r\n  {\r\n    value: \"canceled\",\r\n    label: \"Canceled\",\r\n    icon: XCircle,\r\n  },\r\n]\r\n\r\nexport default function ComboboxPopover() {\r\n  const [open, setOpen] = React.useState(false)\r\n  const [selectedStatus, setSelectedStatus] = React.useState<Status | null>(\r\n    null\r\n  )\r\n\r\n  return (\r\n    <div className=\"flex items-center space-x-4\">\r\n      <p className=\"text-sm text-muted-foreground\">Status</p>\r\n      <Popover open={open} onOpenChange={setOpen}>\r\n        <PopoverTrigger asChild>\r\n          <Button\r\n            variant=\"outline\"\r\n            size=\"sm\"\r\n            className=\"w-[150px] justify-start\"\r\n          >\r\n            {selectedStatus ? (\r\n              <>\r\n                <selectedStatus.icon className=\"mr-2 h-4 w-4 shrink-0\" />\r\n                {selectedStatus.label}\r\n              </>\r\n            ) : (\r\n              <>+ Set status</>\r\n            )}\r\n          </Button>\r\n        </PopoverTrigger>\r\n        <PopoverContent className=\"p-0\" side=\"right\" align=\"start\">\r\n          <Command>\r\n            <CommandInput placeholder=\"Change status...\" />\r\n            <CommandList>\r\n              <CommandEmpty>No results found.</CommandEmpty>\r\n              <CommandGroup>\r\n                {statuses.map((status) => (\r\n                  <CommandItem\r\n                    key={status.value}\r\n                    onSelect={(value) => {\r\n                      setSelectedStatus(\r\n                        statuses.find((priority) => priority.value === value) ||\r\n                          null\r\n                      )\r\n                      setOpen(false)\r\n                    }}\r\n                  >\r\n                    <status.icon\r\n                      className={cn(\r\n                        \"mr-2 h-4 w-4\",\r\n                        status.value === selectedStatus?.value\r\n                          ? \"opacity-100\"\r\n                          : \"opacity-40\"\r\n                      )}\r\n                    />\r\n                    <span>{status.label}</span>\r\n                  </CommandItem>\r\n                ))}\r\n              </CommandGroup>\r\n            </CommandList>\r\n          </Command>\r\n        </PopoverContent>\r\n      </Popover>\r\n    </div>\r\n  )\r\n}"
        }
      ]
    }
  },
  {
    "name": "Command",
    "description": "Fast, composable, unstyled command menu for React.",
    "docs_path": "build\\gits\\shadcn-ui$ui-openv0remix\\docs\\command.mdx",
    "docs": {
      "import": {
        "source": "command.mdx",
        "code": "import {\n  Command,\n  CommandDialog,\n  CommandEmpty,\n  CommandGroup,\n  CommandInput,\n  CommandItem,\n  CommandList,\n  CommandSeparator,\n  CommandShortcut,\n} from \"@/components/ui/command\""
      },
      "use": [
        {
          "source": "command.mdx",
          "code": "<Command>\n  <CommandInput placeholder=\"Type a command or search...\" />\n  <CommandList>\n    <CommandEmpty>No results found.</CommandEmpty>\n    <CommandGroup heading=\"Suggestions\">\n      <CommandItem>Calendar</CommandItem>\n      <CommandItem>Search Emoji</CommandItem>\n      <CommandItem>Calculator</CommandItem>\n    </CommandGroup>\n    <CommandSeparator />\n    <CommandGroup heading=\"Settings\">\n      <CommandItem>Profile</CommandItem>\n      <CommandItem>Billing</CommandItem>\n      <CommandItem>Settings</CommandItem>\n    </CommandGroup>\n  </CommandList>\n</Command>"
        },
        {
          "source": "command.mdx",
          "code": "export function CommandMenu() {\n  const [open, setOpen] = React.useState(false)\n\n  React.useEffect(() => {\n    const down = (e: KeyboardEvent) => {\n      if (e.key === \"k\" && (e.metaKey || e.ctrlKey)) {\n        e.preventDefault()\n        setOpen((open) => !open)\n      }\n    }\n    document.addEventListener(\"keydown\", down)\n    return () => document.removeEventListener(\"keydown\", down)\n  }, [])\n\n  return (\n    <CommandDialog open={open} onOpenChange={setOpen}>\n      <CommandInput placeholder=\"Type a command or search...\" />\n      <CommandList>\n        <CommandEmpty>No results found.</CommandEmpty>\n        <CommandGroup heading=\"Suggestions\">\n          <CommandItem>Calendar</CommandItem>\n          <CommandItem>Search Emoji</CommandItem>\n          <CommandItem>Calculator</CommandItem>\n        </CommandGroup>\n      </CommandList>\n    </CommandDialog>\n  )\n}"
        }
      ],
      "examples": [
        {
          "source": "command-demo.tsx",
          "code": "import {\r\n  Calculator,\r\n  Calendar,\r\n  CreditCard,\r\n  Settings,\r\n  Smile,\r\n  User,\r\n} from \"lucide-react\"\r\n\r\nimport {\r\n  Command,\r\n  CommandEmpty,\r\n  CommandGroup,\r\n  CommandInput,\r\n  CommandItem,\r\n  CommandList,\r\n  CommandSeparator,\r\n  CommandShortcut,\r\n} from \"@/components/ui/command\"\r\n\r\nexport default function CommandDemo() {\r\n  return (\r\n    <Command className=\"rounded-lg border shadow-md\">\r\n      <CommandInput placeholder=\"Type a command or search...\" />\r\n      <CommandList>\r\n        <CommandEmpty>No results found.</CommandEmpty>\r\n        <CommandGroup heading=\"Suggestions\">\r\n          <CommandItem>\r\n            <Calendar className=\"mr-2 h-4 w-4\" />\r\n            <span>Calendar</span>\r\n          </CommandItem>\r\n          <CommandItem>\r\n            <Smile className=\"mr-2 h-4 w-4\" />\r\n            <span>Search Emoji</span>\r\n          </CommandItem>\r\n          <CommandItem>\r\n            <Calculator className=\"mr-2 h-4 w-4\" />\r\n            <span>Calculator</span>\r\n          </CommandItem>\r\n        </CommandGroup>\r\n        <CommandSeparator />\r\n        <CommandGroup heading=\"Settings\">\r\n          <CommandItem>\r\n            <User className=\"mr-2 h-4 w-4\" />\r\n            <span>Profile</span>\r\n            <CommandShortcut>⌘P</CommandShortcut>\r\n          </CommandItem>\r\n          <CommandItem>\r\n            <CreditCard className=\"mr-2 h-4 w-4\" />\r\n            <span>Billing</span>\r\n            <CommandShortcut>⌘B</CommandShortcut>\r\n          </CommandItem>\r\n          <CommandItem>\r\n            <Settings className=\"mr-2 h-4 w-4\" />\r\n            <span>Settings</span>\r\n            <CommandShortcut>⌘S</CommandShortcut>\r\n          </CommandItem>\r\n        </CommandGroup>\r\n      </CommandList>\r\n    </Command>\r\n  )\r\n}"
        },
        {
          "source": "command-dialog.tsx",
          "code": "\"use client\"\r\n\r\nimport * as React from \"react\"\r\nimport {\r\n  Calculator,\r\n  Calendar,\r\n  CreditCard,\r\n  Settings,\r\n  Smile,\r\n  User,\r\n} from \"lucide-react\"\r\n\r\nimport {\r\n  CommandDialog,\r\n  CommandEmpty,\r\n  CommandGroup,\r\n  CommandInput,\r\n  CommandItem,\r\n  CommandList,\r\n  CommandSeparator,\r\n  CommandShortcut,\r\n} from \"@/components/ui/command\"\r\n\r\nexport default function CommandDialogDemo() {\r\n  const [open, setOpen] = React.useState(false)\r\n\r\n  React.useEffect(() => {\r\n    const down = (e: KeyboardEvent) => {\r\n      if (e.key === \"j\" && (e.metaKey || e.ctrlKey)) {\r\n        e.preventDefault()\r\n        setOpen((open) => !open)\r\n      }\r\n    }\r\n\r\n    document.addEventListener(\"keydown\", down)\r\n    return () => document.removeEventListener(\"keydown\", down)\r\n  }, [])\r\n\r\n  return (\r\n    <>\r\n      <p className=\"text-sm text-muted-foreground\">\r\n        Press{\" \"}\r\n        <kbd className=\"pointer-events-none inline-flex h-5 select-none items-center gap-1 rounded border bg-muted px-1.5 font-mono text-[10px] font-medium text-muted-foreground opacity-100\">\r\n          <span className=\"text-xs\">⌘</span>J\r\n        </kbd>\r\n      </p>\r\n      <CommandDialog open={open} onOpenChange={setOpen}>\r\n        <CommandInput placeholder=\"Type a command or search...\" />\r\n        <CommandList>\r\n          <CommandEmpty>No results found.</CommandEmpty>\r\n          <CommandGroup heading=\"Suggestions\">\r\n            <CommandItem>\r\n              <Calendar className=\"mr-2 h-4 w-4\" />\r\n              <span>Calendar</span>\r\n            </CommandItem>\r\n            <CommandItem>\r\n              <Smile className=\"mr-2 h-4 w-4\" />\r\n              <span>Search Emoji</span>\r\n            </CommandItem>\r\n            <CommandItem>\r\n              <Calculator className=\"mr-2 h-4 w-4\" />\r\n              <span>Calculator</span>\r\n            </CommandItem>\r\n          </CommandGroup>\r\n          <CommandSeparator />\r\n          <CommandGroup heading=\"Settings\">\r\n            <CommandItem>\r\n              <User className=\"mr-2 h-4 w-4\" />\r\n              <span>Profile</span>\r\n              <CommandShortcut>⌘P</CommandShortcut>\r\n            </CommandItem>\r\n            <CommandItem>\r\n              <CreditCard className=\"mr-2 h-4 w-4\" />\r\n              <span>Billing</span>\r\n              <CommandShortcut>⌘B</CommandShortcut>\r\n            </CommandItem>\r\n            <CommandItem>\r\n              <Settings className=\"mr-2 h-4 w-4\" />\r\n              <span>Settings</span>\r\n              <CommandShortcut>⌘S</CommandShortcut>\r\n            </CommandItem>\r\n          </CommandGroup>\r\n        </CommandList>\r\n      </CommandDialog>\r\n    </>\r\n  )\r\n}"
        }
      ]
    }
  },
  {
    "name": "Context Menu",
    "description": "Displays a menu to the user — such as a set of actions or functions — triggered by a button.",
    "docs_path": "build\\gits\\shadcn-ui$ui-openv0remix\\docs\\context-menu.mdx",
    "docs": {
      "import": {
        "source": "context-menu.mdx",
        "code": "import {\n  ContextMenu,\n  ContextMenuContent,\n  ContextMenuItem,\n  ContextMenuTrigger,\n} from \"@/components/ui/context-menu\""
      },
      "use": [
        {
          "source": "context-menu.mdx",
          "code": "<ContextMenu>\n  <ContextMenuTrigger>Right click</ContextMenuTrigger>\n  <ContextMenuContent>\n    <ContextMenuItem>Profile</ContextMenuItem>\n    <ContextMenuItem>Billing</ContextMenuItem>\n    <ContextMenuItem>Team</ContextMenuItem>\n    <ContextMenuItem>Subscription</ContextMenuItem>\n  </ContextMenuContent>\n</ContextMenu>"
        }
      ],
      "examples": [
        {
          "source": "context-menu-demo.tsx",
          "code": "import {\r\n  ContextMenu,\r\n  ContextMenuCheckboxItem,\r\n  ContextMenuContent,\r\n  ContextMenuItem,\r\n  ContextMenuLabel,\r\n  ContextMenuRadioGroup,\r\n  ContextMenuRadioItem,\r\n  ContextMenuSeparator,\r\n  ContextMenuShortcut,\r\n  ContextMenuSub,\r\n  ContextMenuSubContent,\r\n  ContextMenuSubTrigger,\r\n  ContextMenuTrigger,\r\n} from \"@/components/ui/context-menu\"\r\n\r\nexport default function ContextMenuDemo() {\r\n  return (\r\n    <ContextMenu>\r\n      <ContextMenuTrigger className=\"flex h-[150px] w-[300px] items-center justify-center rounded-md border border-dashed text-sm\">\r\n        Right click here\r\n      </ContextMenuTrigger>\r\n      <ContextMenuContent className=\"w-64\">\r\n        <ContextMenuItem inset>\r\n          Back\r\n          <ContextMenuShortcut>⌘[</ContextMenuShortcut>\r\n        </ContextMenuItem>\r\n        <ContextMenuItem inset disabled>\r\n          Forward\r\n          <ContextMenuShortcut>⌘]</ContextMenuShortcut>\r\n        </ContextMenuItem>\r\n        <ContextMenuItem inset>\r\n          Reload\r\n          <ContextMenuShortcut>⌘R</ContextMenuShortcut>\r\n        </ContextMenuItem>\r\n        <ContextMenuSub>\r\n          <ContextMenuSubTrigger inset>More Tools</ContextMenuSubTrigger>\r\n          <ContextMenuSubContent className=\"w-48\">\r\n            <ContextMenuItem>\r\n              Save Page As...\r\n              <ContextMenuShortcut>⇧⌘S</ContextMenuShortcut>\r\n            </ContextMenuItem>\r\n            <ContextMenuItem>Create Shortcut...</ContextMenuItem>\r\n            <ContextMenuItem>Name Window...</ContextMenuItem>\r\n            <ContextMenuSeparator />\r\n            <ContextMenuItem>Developer Tools</ContextMenuItem>\r\n          </ContextMenuSubContent>\r\n        </ContextMenuSub>\r\n        <ContextMenuSeparator />\r\n        <ContextMenuCheckboxItem checked>\r\n          Show Bookmarks Bar\r\n          <ContextMenuShortcut>⌘⇧B</ContextMenuShortcut>\r\n        </ContextMenuCheckboxItem>\r\n        <ContextMenuCheckboxItem>Show Full URLs</ContextMenuCheckboxItem>\r\n        <ContextMenuSeparator />\r\n        <ContextMenuRadioGroup value=\"pedro\">\r\n          <ContextMenuLabel inset>People</ContextMenuLabel>\r\n          <ContextMenuSeparator />\r\n          <ContextMenuRadioItem value=\"pedro\">\r\n            Pedro Duarte\r\n          </ContextMenuRadioItem>\r\n          <ContextMenuRadioItem value=\"colm\">Colm Tuite</ContextMenuRadioItem>\r\n        </ContextMenuRadioGroup>\r\n      </ContextMenuContent>\r\n    </ContextMenu>\r\n  )\r\n}"
        }
      ]
    }
  },
  {
    "name": "Date Picker",
    "description": "A date picker component with range and presets.",
    "docs_path": "build\\gits\\shadcn-ui$ui-openv0remix\\docs\\date-picker.mdx",
    "docs": {
      "import": {
        "source": "date-picker.mdx",
        "code": "\"use client\"\n\nimport * as React from \"react\"\nimport { format } from \"date-fns\"\nimport { Calendar as CalendarIcon } from \"lucide-react\"\n\nimport { cn } from \"@/lib/utils\"\nimport { Button } from \"@/components/ui/button\"\nimport { Calendar } from \"@/components/ui/calendar\"\nimport {\n  Popover,\n  PopoverContent,\n  PopoverTrigger,\n} from \"@/components/ui/popover\"\n\nexport function DatePickerDemo() {\n  const [date, setDate] = React.useState<Date>()\n\n  return (\n    <Popover>\n      <PopoverTrigger asChild>\n        <Button\n          variant={\"outline\"}\n          className={cn(\n            \"w-[280px] justify-start text-left font-normal\",\n            !date && \"text-muted-foreground\"\n          )}\n        >\n          <CalendarIcon className=\"mr-2 h-4 w-4\" />\n          {date ? format(date, \"PPP\") : <span>Pick a date</span>}\n        </Button>\n      </PopoverTrigger>\n      <PopoverContent className=\"w-auto p-0\">\n        <Calendar\n          mode=\"single\"\n          selected={date}\n          onSelect={setDate}\n          initialFocus\n        />\n      </PopoverContent>\n    </Popover>\n  )\n}"
      },
      "use": [],
      "examples": [
        {
          "source": "date-picker-demo.tsx",
          "code": "\"use client\"\r\n\r\nimport * as React from \"react\"\r\nimport { format } from \"date-fns\"\r\nimport { Calendar as CalendarIcon } from \"lucide-react\"\r\n\r\nimport { cn } from \"@/lib/utils\"\r\nimport { Button } from \"@/components/ui/button\"\r\nimport { Calendar } from \"@/components/ui/calendar\"\r\nimport {\r\n  Popover,\r\n  PopoverContent,\r\n  PopoverTrigger,\r\n} from \"@/components/ui/popover\"\r\n\r\nexport default function DatePickerDemo() {\r\n  const [date, setDate] = React.useState<Date>()\r\n\r\n  return (\r\n    <Popover>\r\n      <PopoverTrigger asChild>\r\n        <Button\r\n          variant={\"outline\"}\r\n          className={cn(\r\n            \"w-[280px] justify-start text-left font-normal\",\r\n            !date && \"text-muted-foreground\"\r\n          )}\r\n        >\r\n          <CalendarIcon className=\"mr-2 h-4 w-4\" />\r\n          {date ? format(date, \"PPP\") : <span>Pick a date</span>}\r\n        </Button>\r\n      </PopoverTrigger>\r\n      <PopoverContent className=\"w-auto p-0\">\r\n        <Calendar\r\n          mode=\"single\"\r\n          selected={date}\r\n          onSelect={setDate}\r\n          initialFocus\r\n        />\r\n      </PopoverContent>\r\n    </Popover>\r\n  )\r\n}"
        },
        {
          "source": "date-picker-with-presets.tsx",
          "code": "\"use client\"\r\n\r\nimport * as React from \"react\"\r\nimport { addDays, format } from \"date-fns\"\r\nimport { Calendar as CalendarIcon } from \"lucide-react\"\r\n\r\nimport { cn } from \"@/lib/utils\"\r\nimport { Button } from \"@/components/ui/button\"\r\nimport { Calendar } from \"@/components/ui/calendar\"\r\nimport {\r\n  Popover,\r\n  PopoverContent,\r\n  PopoverTrigger,\r\n} from \"@/components/ui/popover\"\r\nimport {\r\n  Select,\r\n  SelectContent,\r\n  SelectItem,\r\n  SelectTrigger,\r\n  SelectValue,\r\n} from \"@/components/ui/select\"\r\n\r\nexport default function DatePickerWithPresets() {\r\n  const [date, setDate] = React.useState<Date>()\r\n\r\n  return (\r\n    <Popover>\r\n      <PopoverTrigger asChild>\r\n        <Button\r\n          variant={\"outline\"}\r\n          className={cn(\r\n            \"w-[280px] justify-start text-left font-normal\",\r\n            !date && \"text-muted-foreground\"\r\n          )}\r\n        >\r\n          <CalendarIcon className=\"mr-2 h-4 w-4\" />\r\n          {date ? format(date, \"PPP\") : <span>Pick a date</span>}\r\n        </Button>\r\n      </PopoverTrigger>\r\n      <PopoverContent className=\"flex w-auto flex-col space-y-2 p-2\">\r\n        <Select\r\n          onValueChange={(value) =>\r\n            setDate(addDays(new Date(), parseInt(value)))\r\n          }\r\n        >\r\n          <SelectTrigger>\r\n            <SelectValue placeholder=\"Select\" />\r\n          </SelectTrigger>\r\n          <SelectContent position=\"popper\">\r\n            <SelectItem value=\"0\">Today</SelectItem>\r\n            <SelectItem value=\"1\">Tomorrow</SelectItem>\r\n            <SelectItem value=\"3\">In 3 days</SelectItem>\r\n            <SelectItem value=\"7\">In a week</SelectItem>\r\n          </SelectContent>\r\n        </Select>\r\n        <div className=\"rounded-md border\">\r\n          <Calendar mode=\"single\" selected={date} onSelect={setDate} />\r\n        </div>\r\n      </PopoverContent>\r\n    </Popover>\r\n  )\r\n}"
        },
        {
          "source": "date-picker-with-range.tsx",
          "code": "\"use client\"\r\n\r\nimport * as React from \"react\"\r\nimport { addDays, format } from \"date-fns\"\r\nimport { Calendar as CalendarIcon } from \"lucide-react\"\r\nimport { DateRange } from \"react-day-picker\"\r\n\r\nimport { cn } from \"@/lib/utils\"\r\nimport { Button } from \"@/components/ui/button\"\r\nimport { Calendar } from \"@/components/ui/calendar\"\r\nimport {\r\n  Popover,\r\n  PopoverContent,\r\n  PopoverTrigger,\r\n} from \"@/components/ui/popover\"\r\n\r\nexport default function DatePickerWithRange({\r\n  className,\r\n}: React.HTMLAttributes<HTMLDivElement>) {\r\n  const [date, setDate] = React.useState<DateRange | undefined>({\r\n    from: new Date(2022, 0, 20),\r\n    to: addDays(new Date(2022, 0, 20), 20),\r\n  })\r\n\r\n  return (\r\n    <div className={cn(\"grid gap-2\", className)}>\r\n      <Popover>\r\n        <PopoverTrigger asChild>\r\n          <Button\r\n            id=\"date\"\r\n            variant={\"outline\"}\r\n            className={cn(\r\n              \"w-[300px] justify-start text-left font-normal\",\r\n              !date && \"text-muted-foreground\"\r\n            )}\r\n          >\r\n            <CalendarIcon className=\"mr-2 h-4 w-4\" />\r\n            {date?.from ? (\r\n              date.to ? (\r\n                <>\r\n                  {format(date.from, \"LLL dd, y\")} -{\" \"}\r\n                  {format(date.to, \"LLL dd, y\")}\r\n                </>\r\n              ) : (\r\n                format(date.from, \"LLL dd, y\")\r\n              )\r\n            ) : (\r\n              <span>Pick a date</span>\r\n            )}\r\n          </Button>\r\n        </PopoverTrigger>\r\n        <PopoverContent className=\"w-auto p-0\" align=\"start\">\r\n          <Calendar\r\n            initialFocus\r\n            mode=\"range\"\r\n            defaultMonth={date?.from}\r\n            selected={date}\r\n            onSelect={setDate}\r\n            numberOfMonths={2}\r\n          />\r\n        </PopoverContent>\r\n      </Popover>\r\n    </div>\r\n  )\r\n}"
        }
      ]
    }
  },
  {
    "name": "Dialog",
    "description": "A window overlaid on either the primary window or another dialog window, rendering the content underneath inert.",
    "docs_path": "build\\gits\\shadcn-ui$ui-openv0remix\\docs\\dialog.mdx",
    "docs": {
      "import": {
        "source": "dialog.mdx",
        "code": "import {\n  Dialog,\n  DialogContent,\n  DialogDescription,\n  DialogHeader,\n  DialogTitle,\n  DialogTrigger,\n} from \"@/components/ui/dialog\""
      },
      "use": [
        {
          "source": "dialog.mdx",
          "code": "<Dialog>\n  <DialogTrigger>Open</DialogTrigger>\n  <DialogContent>\n    <DialogHeader>\n      <DialogTitle>Are you sure absolutely sure?</DialogTitle>\n      <DialogDescription>\n        This action cannot be undone. This will permanently delete your account\n        and remove your data from our servers.\n      </DialogDescription>\n    </DialogHeader>\n  </DialogContent>\n</Dialog>"
        }
      ],
      "examples": [
        {
          "source": "dialog-demo.tsx",
          "code": "import { Button } from \"@/components/ui/button\"\r\nimport {\r\n  Dialog,\r\n  DialogContent,\r\n  DialogDescription,\r\n  DialogFooter,\r\n  DialogHeader,\r\n  DialogTitle,\r\n  DialogTrigger,\r\n} from \"@/components/ui/dialog\"\r\nimport { Input } from \"@/components/ui/input\"\r\nimport { Label } from \"@/components/ui/label\"\r\n\r\nexport default function DialogDemo() {\r\n  return (\r\n    <Dialog>\r\n      <DialogTrigger asChild>\r\n        <Button variant=\"outline\">Edit Profile</Button>\r\n      </DialogTrigger>\r\n      <DialogContent className=\"sm:max-w-[425px]\">\r\n        <DialogHeader>\r\n          <DialogTitle>Edit profile</DialogTitle>\r\n          <DialogDescription>\r\n            Make changes to your profile here. Click save when you're done.\r\n          </DialogDescription>\r\n        </DialogHeader>\r\n        <div className=\"grid gap-4 py-4\">\r\n          <div className=\"grid grid-cols-4 items-center gap-4\">\r\n            <Label htmlFor=\"name\" className=\"text-right\">\r\n              Name\r\n            </Label>\r\n            <Input id=\"name\" value=\"Pedro Duarte\" className=\"col-span-3\" />\r\n          </div>\r\n          <div className=\"grid grid-cols-4 items-center gap-4\">\r\n            <Label htmlFor=\"username\" className=\"text-right\">\r\n              Username\r\n            </Label>\r\n            <Input id=\"username\" value=\"@peduarte\" className=\"col-span-3\" />\r\n          </div>\r\n        </div>\r\n        <DialogFooter>\r\n          <Button type=\"submit\">Save changes</Button>\r\n        </DialogFooter>\r\n      </DialogContent>\r\n    </Dialog>\r\n  )\r\n}"
        }
      ]
    }
  },
  {
    "name": "Dropdown Menu",
    "description": "Displays a menu to the user — such as a set of actions or functions — triggered by a button.",
    "docs_path": "build\\gits\\shadcn-ui$ui-openv0remix\\docs\\dropdown-menu.mdx",
    "docs": {
      "import": {
        "source": "dropdown-menu.mdx",
        "code": "import {\n  DropdownMenu,\n  DropdownMenuContent,\n  DropdownMenuItem,\n  DropdownMenuLabel,\n  DropdownMenuSeparator,\n  DropdownMenuTrigger,\n} from \"@/components/ui/dropdown-menu\""
      },
      "use": [
        {
          "source": "dropdown-menu.mdx",
          "code": "<DropdownMenu>\n  <DropdownMenuTrigger>Open</DropdownMenuTrigger>\n  <DropdownMenuContent>\n    <DropdownMenuLabel>My Account</DropdownMenuLabel>\n    <DropdownMenuSeparator />\n    <DropdownMenuItem>Profile</DropdownMenuItem>\n    <DropdownMenuItem>Billing</DropdownMenuItem>\n    <DropdownMenuItem>Team</DropdownMenuItem>\n    <DropdownMenuItem>Subscription</DropdownMenuItem>\n  </DropdownMenuContent>\n</DropdownMenu>"
        }
      ],
      "examples": [
        {
          "source": "dropdown-menu-checkboxes.tsx",
          "code": "\"use client\"\r\n\r\nimport * as React from \"react\"\r\nimport { DropdownMenuCheckboxItemProps } from \"@radix-ui/react-dropdown-menu\"\r\n\r\nimport { Button } from \"@/components/ui/button\"\r\nimport {\r\n  DropdownMenu,\r\n  DropdownMenuCheckboxItem,\r\n  DropdownMenuContent,\r\n  DropdownMenuLabel,\r\n  DropdownMenuSeparator,\r\n  DropdownMenuTrigger,\r\n} from \"@/components/ui/dropdown-menu\"\r\n\r\ntype Checked = DropdownMenuCheckboxItemProps[\"checked\"]\r\n\r\nexport default function DropdownMenuCheckboxes() {\r\n  const [showStatusBar, setShowStatusBar] = React.useState<Checked>(true)\r\n  const [showActivityBar, setShowActivityBar] = React.useState<Checked>(false)\r\n  const [showPanel, setShowPanel] = React.useState<Checked>(false)\r\n\r\n  return (\r\n    <DropdownMenu>\r\n      <DropdownMenuTrigger asChild>\r\n        <Button variant=\"outline\">Open</Button>\r\n      </DropdownMenuTrigger>\r\n      <DropdownMenuContent className=\"w-56\">\r\n        <DropdownMenuLabel>Appearance</DropdownMenuLabel>\r\n        <DropdownMenuSeparator />\r\n        <DropdownMenuCheckboxItem\r\n          checked={showStatusBar}\r\n          onCheckedChange={setShowStatusBar}\r\n        >\r\n          Status Bar\r\n        </DropdownMenuCheckboxItem>\r\n        <DropdownMenuCheckboxItem\r\n          checked={showActivityBar}\r\n          onCheckedChange={setShowActivityBar}\r\n          disabled\r\n        >\r\n          Activity Bar\r\n        </DropdownMenuCheckboxItem>\r\n        <DropdownMenuCheckboxItem\r\n          checked={showPanel}\r\n          onCheckedChange={setShowPanel}\r\n        >\r\n          Panel\r\n        </DropdownMenuCheckboxItem>\r\n      </DropdownMenuContent>\r\n    </DropdownMenu>\r\n  )\r\n}"
        },
        {
          "source": "dropdown-menu-demo.tsx",
          "code": "import {\r\n  Cloud,\r\n  CreditCard,\r\n  Github,\r\n  Keyboard,\r\n  LifeBuoy,\r\n  LogOut,\r\n  Mail,\r\n  MessageSquare,\r\n  Plus,\r\n  PlusCircle,\r\n  Settings,\r\n  User,\r\n  UserPlus,\r\n  Users,\r\n} from \"lucide-react\"\r\n\r\nimport { Button } from \"@/components/ui/button\"\r\nimport {\r\n  DropdownMenu,\r\n  DropdownMenuContent,\r\n  DropdownMenuGroup,\r\n  DropdownMenuItem,\r\n  DropdownMenuLabel,\r\n  DropdownMenuPortal,\r\n  DropdownMenuSeparator,\r\n  DropdownMenuShortcut,\r\n  DropdownMenuSub,\r\n  DropdownMenuSubContent,\r\n  DropdownMenuSubTrigger,\r\n  DropdownMenuTrigger,\r\n} from \"@/components/ui/dropdown-menu\"\r\n\r\nexport default function DropdownMenuDemo() {\r\n  return (\r\n    <DropdownMenu>\r\n      <DropdownMenuTrigger asChild>\r\n        <Button variant=\"outline\">Open</Button>\r\n      </DropdownMenuTrigger>\r\n      <DropdownMenuContent className=\"w-56\">\r\n        <DropdownMenuLabel>My Account</DropdownMenuLabel>\r\n        <DropdownMenuSeparator />\r\n        <DropdownMenuGroup>\r\n          <DropdownMenuItem>\r\n            <User className=\"mr-2 h-4 w-4\" />\r\n            <span>Profile</span>\r\n            <DropdownMenuShortcut>⇧⌘P</DropdownMenuShortcut>\r\n          </DropdownMenuItem>\r\n          <DropdownMenuItem>\r\n            <CreditCard className=\"mr-2 h-4 w-4\" />\r\n            <span>Billing</span>\r\n            <DropdownMenuShortcut>⌘B</DropdownMenuShortcut>\r\n          </DropdownMenuItem>\r\n          <DropdownMenuItem>\r\n            <Settings className=\"mr-2 h-4 w-4\" />\r\n            <span>Settings</span>\r\n            <DropdownMenuShortcut>⌘S</DropdownMenuShortcut>\r\n          </DropdownMenuItem>\r\n          <DropdownMenuItem>\r\n            <Keyboard className=\"mr-2 h-4 w-4\" />\r\n            <span>Keyboard shortcuts</span>\r\n            <DropdownMenuShortcut>⌘K</DropdownMenuShortcut>\r\n          </DropdownMenuItem>\r\n        </DropdownMenuGroup>\r\n        <DropdownMenuSeparator />\r\n        <DropdownMenuGroup>\r\n          <DropdownMenuItem>\r\n            <Users className=\"mr-2 h-4 w-4\" />\r\n            <span>Team</span>\r\n          </DropdownMenuItem>\r\n          <DropdownMenuSub>\r\n            <DropdownMenuSubTrigger>\r\n              <UserPlus className=\"mr-2 h-4 w-4\" />\r\n              <span>Invite users</span>\r\n            </DropdownMenuSubTrigger>\r\n            <DropdownMenuPortal>\r\n              <DropdownMenuSubContent>\r\n                <DropdownMenuItem>\r\n                  <Mail className=\"mr-2 h-4 w-4\" />\r\n                  <span>Email</span>\r\n                </DropdownMenuItem>\r\n                <DropdownMenuItem>\r\n                  <MessageSquare className=\"mr-2 h-4 w-4\" />\r\n                  <span>Message</span>\r\n                </DropdownMenuItem>\r\n                <DropdownMenuSeparator />\r\n                <DropdownMenuItem>\r\n                  <PlusCircle className=\"mr-2 h-4 w-4\" />\r\n                  <span>More...</span>\r\n                </DropdownMenuItem>\r\n              </DropdownMenuSubContent>\r\n            </DropdownMenuPortal>\r\n          </DropdownMenuSub>\r\n          <DropdownMenuItem>\r\n            <Plus className=\"mr-2 h-4 w-4\" />\r\n            <span>New Team</span>\r\n            <DropdownMenuShortcut>⌘+T</DropdownMenuShortcut>\r\n          </DropdownMenuItem>\r\n        </DropdownMenuGroup>\r\n        <DropdownMenuSeparator />\r\n        <DropdownMenuItem>\r\n          <Github className=\"mr-2 h-4 w-4\" />\r\n          <span>GitHub</span>\r\n        </DropdownMenuItem>\r\n        <DropdownMenuItem>\r\n          <LifeBuoy className=\"mr-2 h-4 w-4\" />\r\n          <span>Support</span>\r\n        </DropdownMenuItem>\r\n        <DropdownMenuItem disabled>\r\n          <Cloud className=\"mr-2 h-4 w-4\" />\r\n          <span>API</span>\r\n        </DropdownMenuItem>\r\n        <DropdownMenuSeparator />\r\n        <DropdownMenuItem>\r\n          <LogOut className=\"mr-2 h-4 w-4\" />\r\n          <span>Log out</span>\r\n          <DropdownMenuShortcut>⇧⌘Q</DropdownMenuShortcut>\r\n        </DropdownMenuItem>\r\n      </DropdownMenuContent>\r\n    </DropdownMenu>\r\n  )\r\n}"
        },
        {
          "source": "dropdown-menu-radio-group.tsx",
          "code": "\"use client\"\r\n\r\nimport * as React from \"react\"\r\nimport { DropdownMenuCheckboxItemProps } from \"@radix-ui/react-dropdown-menu\"\r\n\r\nimport { Button } from \"@/components/ui/button\"\r\nimport {\r\n  DropdownMenu,\r\n  DropdownMenuCheckboxItem,\r\n  DropdownMenuContent,\r\n  DropdownMenuLabel,\r\n  DropdownMenuRadioGroup,\r\n  DropdownMenuRadioItem,\r\n  DropdownMenuSeparator,\r\n  DropdownMenuTrigger,\r\n} from \"@/components/ui/dropdown-menu\"\r\n\r\nexport default function DropdownMenuRadioGroupDemo() {\r\n  const [position, setPosition] = React.useState(\"bottom\")\r\n\r\n  return (\r\n    <DropdownMenu>\r\n      <DropdownMenuTrigger asChild>\r\n        <Button variant=\"outline\">Open</Button>\r\n      </DropdownMenuTrigger>\r\n      <DropdownMenuContent className=\"w-56\">\r\n        <DropdownMenuLabel>Panel Position</DropdownMenuLabel>\r\n        <DropdownMenuSeparator />\r\n        <DropdownMenuRadioGroup value={position} onValueChange={setPosition}>\r\n          <DropdownMenuRadioItem value=\"top\">Top</DropdownMenuRadioItem>\r\n          <DropdownMenuRadioItem value=\"bottom\">Bottom</DropdownMenuRadioItem>\r\n          <DropdownMenuRadioItem value=\"right\">Right</DropdownMenuRadioItem>\r\n        </DropdownMenuRadioGroup>\r\n      </DropdownMenuContent>\r\n    </DropdownMenu>\r\n  )\r\n}"
        }
      ]
    }
  },
  {
    "name": "Hover Card",
    "description": "For sighted users to preview content available behind a link.",
    "docs_path": "build\\gits\\shadcn-ui$ui-openv0remix\\docs\\hover-card.mdx",
    "docs": {
      "import": {
        "source": "hover-card.mdx",
        "code": "import {\n  HoverCard,\n  HoverCardContent,\n  HoverCardTrigger,\n} from \"@/components/ui/hover-card\""
      },
      "use": [
        {
          "source": "hover-card.mdx",
          "code": "<HoverCard>\n  <HoverCardTrigger>Hover</HoverCardTrigger>\n  <HoverCardContent>\n    The React Framework – created and maintained by @vercel.\n  </HoverCardContent>\n</HoverCard>"
        }
      ],
      "examples": [
        {
          "source": "hover-card-demo.tsx",
          "code": "import { CalendarDays } from \"lucide-react\"\r\n\r\nimport {\r\n  Avatar,\r\n  AvatarFallback,\r\n  AvatarImage,\r\n} from \"@/components/ui/avatar\"\r\nimport { Button } from \"@/components/ui/button\"\r\nimport {\r\n  HoverCard,\r\n  HoverCardContent,\r\n  HoverCardTrigger,\r\n} from \"@/components/ui/hover-card\"\r\n\r\nexport default function HoverCardDemo() {\r\n  return (\r\n    <HoverCard>\r\n      <HoverCardTrigger asChild>\r\n        <Button variant=\"link\">@nextjs</Button>\r\n      </HoverCardTrigger>\r\n      <HoverCardContent className=\"w-80\">\r\n        <div className=\"flex justify-between space-x-4\">\r\n          <Avatar>\r\n            <AvatarImage src=\"https://github.com/vercel.png\" />\r\n            <AvatarFallback>VC</AvatarFallback>\r\n          </Avatar>\r\n          <div className=\"space-y-1\">\r\n            <h4 className=\"text-sm font-semibold\">@nextjs</h4>\r\n            <p className=\"text-sm\">\r\n              The React Framework – created and maintained by @vercel.\r\n            </p>\r\n            <div className=\"flex items-center pt-2\">\r\n              <CalendarDays className=\"mr-2 h-4 w-4 opacity-70\" />{\" \"}\r\n              <span className=\"text-xs text-muted-foreground\">\r\n                Joined December 2021\r\n              </span>\r\n            </div>\r\n          </div>\r\n        </div>\r\n      </HoverCardContent>\r\n    </HoverCard>\r\n  )\r\n}"
        }
      ]
    }
  },
  {
    "name": "Input",
    "description": "Displays a form input field or a component that looks like an input field.",
    "docs_path": "build\\gits\\shadcn-ui$ui-openv0remix\\docs\\input.mdx",
    "docs": {
      "import": {
        "source": "input.mdx",
        "code": "import { Input } from \"@/components/ui/input\""
      },
      "use": [{ "source": "input.mdx", "code": "<Input />" }],
      "examples": [
        {
          "source": "input-demo.tsx",
          "code": "import { Input } from \"@/components/ui/input\"\r\n\r\nexport default function InputDemo() {\r\n  return <Input type=\"email\" placeholder=\"Email\" />\r\n}"
        },
        {
          "source": "input-disabled.tsx",
          "code": "import { Input } from \"@/components/ui/input\"\r\n\r\nexport default function InputDisabled() {\r\n  return <Input disabled type=\"email\" placeholder=\"Email\" />\r\n}"
        },
        {
          "source": "input-file.tsx",
          "code": "import { Input } from \"@/components/ui/input\"\r\nimport { Label } from \"@/components/ui/label\"\r\n\r\nexport default function InputFile() {\r\n  return (\r\n    <div className=\"grid w-full max-w-sm items-center gap-1.5\">\r\n      <Label htmlFor=\"picture\">Picture</Label>\r\n      <Input id=\"picture\" type=\"file\" />\r\n    </div>\r\n  )\r\n}"
        },
        {
          "source": "input-with-button.tsx",
          "code": "import { Button } from \"@/components/ui/button\"\r\nimport { Input } from \"@/components/ui/input\"\r\n\r\nexport default function InputWithButton() {\r\n  return (\r\n    <div className=\"flex w-full max-w-sm items-center space-x-2\">\r\n      <Input type=\"email\" placeholder=\"Email\" />\r\n      <Button type=\"submit\">Subscribe</Button>\r\n    </div>\r\n  )\r\n}"
        },
        {
          "source": "input-with-label.tsx",
          "code": "import { Input } from \"@/components/ui/input\"\r\nimport { Label } from \"@/components/ui/label\"\r\n\r\nexport default function InputWithLabel() {\r\n  return (\r\n    <div className=\"grid w-full max-w-sm items-center gap-1.5\">\r\n      <Label htmlFor=\"email\">Email</Label>\r\n      <Input type=\"email\" id=\"email\" placeholder=\"Email\" />\r\n    </div>\r\n  )\r\n}"
        },
        {
          "source": "input-with-text.tsx",
          "code": "import { Input } from \"@/components/ui/input\"\r\nimport { Label } from \"@/components/ui/label\"\r\n\r\nexport default function InputWithText() {\r\n  return (\r\n    <div className=\"grid w-full max-w-sm items-center gap-1.5\">\r\n      <Label htmlFor=\"email-2\">Email</Label>\r\n      <Input type=\"email\" id=\"email-2\" placeholder=\"Email\" />\r\n      <p className=\"text-sm text-muted-foreground\">Enter your email address.</p>\r\n    </div>\r\n  )\r\n}"
        }
      ]
    }
  },
  {
    "name": "Label",
    "description": "Renders an accessible label associated with controls.",
    "docs_path": "build\\gits\\shadcn-ui$ui-openv0remix\\docs\\label.mdx",
    "docs": {
      "import": {
        "source": "label.mdx",
        "code": "import { Label } from \"@/components/ui/label\""
      },
      "use": [
        {
          "source": "label.mdx",
          "code": "<Label htmlFor=\"email\">Your email address</Label>"
        }
      ],
      "examples": [
        {
          "source": "label-demo.tsx",
          "code": "import { Checkbox } from \"@/components/ui/checkbox\"\r\nimport { Label } from \"@/components/ui/label\"\r\n\r\nexport default function LabelDemo() {\r\n  return (\r\n    <div>\r\n      <div className=\"flex items-center space-x-2\">\r\n        <Checkbox id=\"terms\" />\r\n        <Label htmlFor=\"terms\">Accept terms and conditions</Label>\r\n      </div>\r\n    </div>\r\n  )\r\n}"
        }
      ]
    }
  },
  {
    "name": "Menubar",
    "description": "A visually persistent menu common in desktop applications that provides quick access to a consistent set of commands.",
    "docs_path": "build\\gits\\shadcn-ui$ui-openv0remix\\docs\\menubar.mdx",
    "docs": {
      "import": {
        "source": "menubar.mdx",
        "code": "import {\n  Menubar,\n  MenubarContent,\n  MenubarItem,\n  MenubarMenu,\n  MenubarSeparator,\n  MenubarShortcut,\n  MenubarTrigger,\n} from \"@/components/ui/menubar\""
      },
      "use": [
        {
          "source": "menubar.mdx",
          "code": "<Menubar>\n  <MenubarMenu>\n    <MenubarTrigger>File</MenubarTrigger>\n    <MenubarContent>\n      <MenubarItem>\n        New Tab <MenubarShortcut>⌘T</MenubarShortcut>\n      </MenubarItem>\n      <MenubarItem>New Window</MenubarItem>\n      <MenubarSeparator />\n      <MenubarItem>Share</MenubarItem>\n      <MenubarSeparator />\n      <MenubarItem>Print</MenubarItem>\n    </MenubarContent>\n  </MenubarMenu>\n</Menubar>"
        }
      ],
      "examples": [
        {
          "source": "menubar-demo.tsx",
          "code": "import {\r\n  Menubar,\r\n  MenubarCheckboxItem,\r\n  MenubarContent,\r\n  MenubarItem,\r\n  MenubarMenu,\r\n  MenubarRadioGroup,\r\n  MenubarRadioItem,\r\n  MenubarSeparator,\r\n  MenubarShortcut,\r\n  MenubarSub,\r\n  MenubarSubContent,\r\n  MenubarSubTrigger,\r\n  MenubarTrigger,\r\n} from \"@/components/ui/menubar\"\r\n\r\nexport default function MenubarDemo() {\r\n  return (\r\n    <Menubar>\r\n      <MenubarMenu>\r\n        <MenubarTrigger>File</MenubarTrigger>\r\n        <MenubarContent>\r\n          <MenubarItem>\r\n            New Tab <MenubarShortcut>⌘T</MenubarShortcut>\r\n          </MenubarItem>\r\n          <MenubarItem>\r\n            New Window <MenubarShortcut>⌘N</MenubarShortcut>\r\n          </MenubarItem>\r\n          <MenubarItem disabled>New Incognito Window</MenubarItem>\r\n          <MenubarSeparator />\r\n          <MenubarSub>\r\n            <MenubarSubTrigger>Share</MenubarSubTrigger>\r\n            <MenubarSubContent>\r\n              <MenubarItem>Email link</MenubarItem>\r\n              <MenubarItem>Messages</MenubarItem>\r\n              <MenubarItem>Notes</MenubarItem>\r\n            </MenubarSubContent>\r\n          </MenubarSub>\r\n          <MenubarSeparator />\r\n          <MenubarItem>\r\n            Print... <MenubarShortcut>⌘P</MenubarShortcut>\r\n          </MenubarItem>\r\n        </MenubarContent>\r\n      </MenubarMenu>\r\n      <MenubarMenu>\r\n        <MenubarTrigger>Edit</MenubarTrigger>\r\n        <MenubarContent>\r\n          <MenubarItem>\r\n            Undo <MenubarShortcut>⌘Z</MenubarShortcut>\r\n          </MenubarItem>\r\n          <MenubarItem>\r\n            Redo <MenubarShortcut>⇧⌘Z</MenubarShortcut>\r\n          </MenubarItem>\r\n          <MenubarSeparator />\r\n          <MenubarSub>\r\n            <MenubarSubTrigger>Find</MenubarSubTrigger>\r\n            <MenubarSubContent>\r\n              <MenubarItem>Search the web</MenubarItem>\r\n              <MenubarSeparator />\r\n              <MenubarItem>Find...</MenubarItem>\r\n              <MenubarItem>Find Next</MenubarItem>\r\n              <MenubarItem>Find Previous</MenubarItem>\r\n            </MenubarSubContent>\r\n          </MenubarSub>\r\n          <MenubarSeparator />\r\n          <MenubarItem>Cut</MenubarItem>\r\n          <MenubarItem>Copy</MenubarItem>\r\n          <MenubarItem>Paste</MenubarItem>\r\n        </MenubarContent>\r\n      </MenubarMenu>\r\n      <MenubarMenu>\r\n        <MenubarTrigger>View</MenubarTrigger>\r\n        <MenubarContent>\r\n          <MenubarCheckboxItem>Always Show Bookmarks Bar</MenubarCheckboxItem>\r\n          <MenubarCheckboxItem checked>\r\n            Always Show Full URLs\r\n          </MenubarCheckboxItem>\r\n          <MenubarSeparator />\r\n          <MenubarItem inset>\r\n            Reload <MenubarShortcut>⌘R</MenubarShortcut>\r\n          </MenubarItem>\r\n          <MenubarItem disabled inset>\r\n            Force Reload <MenubarShortcut>⇧⌘R</MenubarShortcut>\r\n          </MenubarItem>\r\n          <MenubarSeparator />\r\n          <MenubarItem inset>Toggle Fullscreen</MenubarItem>\r\n          <MenubarSeparator />\r\n          <MenubarItem inset>Hide Sidebar</MenubarItem>\r\n        </MenubarContent>\r\n      </MenubarMenu>\r\n      <MenubarMenu>\r\n        <MenubarTrigger>Profiles</MenubarTrigger>\r\n        <MenubarContent>\r\n          <MenubarRadioGroup value=\"benoit\">\r\n            <MenubarRadioItem value=\"andy\">Andy</MenubarRadioItem>\r\n            <MenubarRadioItem value=\"benoit\">Benoit</MenubarRadioItem>\r\n            <MenubarRadioItem value=\"Luis\">Luis</MenubarRadioItem>\r\n          </MenubarRadioGroup>\r\n          <MenubarSeparator />\r\n          <MenubarItem inset>Edit...</MenubarItem>\r\n          <MenubarSeparator />\r\n          <MenubarItem inset>Add Profile...</MenubarItem>\r\n        </MenubarContent>\r\n      </MenubarMenu>\r\n    </Menubar>\r\n  )\r\n}"
        }
      ]
    }
  },
  {
    "name": "Navigation Menu",
    "description": "A collection of links for navigating websites.",
    "docs_path": "build\\gits\\shadcn-ui$ui-openv0remix\\docs\\navigation-menu.mdx",
    "docs": {
      "import": {
        "source": "navigation-menu.mdx",
        "code": "import {\n  NavigationMenu,\n  NavigationMenuContent,\n  NavigationMenuIndicator,\n  NavigationMenuItem,\n  NavigationMenuLink,\n  NavigationMenuList,\n  NavigationMenuTrigger,\n  NavigationMenuViewport,\n} from \"@/components/ui/navigation-menu\""
      },
      "use": [
        {
          "source": "navigation-menu.mdx",
          "code": "<NavigationMenu>\n  <NavigationMenuList>\n    <NavigationMenuItem>\n      <NavigationMenuTrigger>Item One</NavigationMenuTrigger>\n      <NavigationMenuContent>\n        <NavigationMenuLink>Link</NavigationMenuLink>\n      </NavigationMenuContent>\n    </NavigationMenuItem>\n  </NavigationMenuList>\n</NavigationMenu>"
        },
        {
          "source": "navigation-menu.mdx",
          "code": "import { navigationMenuTriggerStyle } from \"@/components/ui/navigation-menu\""
        }
      ],
      "examples": []
    }
  },
  {
    "name": "Popover",
    "description": "Displays rich content in a portal, triggered by a button.",
    "docs_path": "build\\gits\\shadcn-ui$ui-openv0remix\\docs\\popover.mdx",
    "docs": {
      "import": {
        "source": "popover.mdx",
        "code": "import {\n  Popover,\n  PopoverContent,\n  PopoverTrigger,\n} from \"@/components/ui/popover\""
      },
      "use": [
        {
          "source": "popover.mdx",
          "code": "<Popover>\n  <PopoverTrigger>Open</PopoverTrigger>\n  <PopoverContent>Place content for the popover here.</PopoverContent>\n</Popover>"
        }
      ],
      "examples": [
        {
          "source": "popover-demo.tsx",
          "code": "import { Button } from \"@/components/ui/button\"\r\nimport { Input } from \"@/components/ui/input\"\r\nimport { Label } from \"@/components/ui/label\"\r\nimport {\r\n  Popover,\r\n  PopoverContent,\r\n  PopoverTrigger,\r\n} from \"@/components/ui/popover\"\r\n\r\nexport default function PopoverDemo() {\r\n  return (\r\n    <Popover>\r\n      <PopoverTrigger asChild>\r\n        <Button variant=\"outline\">Open popover</Button>\r\n      </PopoverTrigger>\r\n      <PopoverContent className=\"w-80\">\r\n        <div className=\"grid gap-4\">\r\n          <div className=\"space-y-2\">\r\n            <h4 className=\"font-medium leading-none\">Dimensions</h4>\r\n            <p className=\"text-sm text-muted-foreground\">\r\n              Set the dimensions for the layer.\r\n            </p>\r\n          </div>\r\n          <div className=\"grid gap-2\">\r\n            <div className=\"grid grid-cols-3 items-center gap-4\">\r\n              <Label htmlFor=\"width\">Width</Label>\r\n              <Input\r\n                id=\"width\"\r\n                defaultValue=\"100%\"\r\n                className=\"col-span-2 h-8\"\r\n              />\r\n            </div>\r\n            <div className=\"grid grid-cols-3 items-center gap-4\">\r\n              <Label htmlFor=\"maxWidth\">Max. width</Label>\r\n              <Input\r\n                id=\"maxWidth\"\r\n                defaultValue=\"300px\"\r\n                className=\"col-span-2 h-8\"\r\n              />\r\n            </div>\r\n            <div className=\"grid grid-cols-3 items-center gap-4\">\r\n              <Label htmlFor=\"height\">Height</Label>\r\n              <Input\r\n                id=\"height\"\r\n                defaultValue=\"25px\"\r\n                className=\"col-span-2 h-8\"\r\n              />\r\n            </div>\r\n            <div className=\"grid grid-cols-3 items-center gap-4\">\r\n              <Label htmlFor=\"maxHeight\">Max. height</Label>\r\n              <Input\r\n                id=\"maxHeight\"\r\n                defaultValue=\"none\"\r\n                className=\"col-span-2 h-8\"\r\n              />\r\n            </div>\r\n          </div>\r\n        </div>\r\n      </PopoverContent>\r\n    </Popover>\r\n  )\r\n}"
        }
      ]
    }
  },
  {
    "name": "Progress",
    "description": "Displays an indicator showing the completion progress of a task, typically displayed as a progress bar.",
    "docs_path": "build\\gits\\shadcn-ui$ui-openv0remix\\docs\\progress.mdx",
    "docs": {
      "import": {
        "source": "progress.mdx",
        "code": "import { Progress } from \"@/components/ui/progress\""
      },
      "use": [{ "source": "progress.mdx", "code": "<Progress value={33} />" }],
      "examples": [
        {
          "source": "progress-demo.tsx",
          "code": "\"use client\"\r\n\r\nimport * as React from \"react\"\r\n\r\nimport { Progress } from \"@/components/ui/progress\"\r\n\r\nexport default function ProgressDemo() {\r\n  const [progress, setProgress] = React.useState(13)\r\n\r\n  React.useEffect(() => {\r\n    const timer = setTimeout(() => setProgress(66), 500)\r\n    return () => clearTimeout(timer)\r\n  }, [])\r\n\r\n  return <Progress value={progress} className=\"w-[60%]\" />\r\n}"
        }
      ]
    }
  },
  {
    "name": "Radio Group",
    "description": "A set of checkable buttons—known as radio buttons—where no more than one of the buttons can be checked at a time.",
    "docs_path": "build\\gits\\shadcn-ui$ui-openv0remix\\docs\\radio-group.mdx",
    "docs": {
      "import": {
        "source": "radio-group.mdx",
        "code": "import { Label } from \"@/components/ui/label\"\nimport { RadioGroup, RadioGroupItem } from \"@/components/ui/radio-group\""
      },
      "use": [
        {
          "source": "radio-group.mdx",
          "code": "<RadioGroup defaultValue=\"option-one\">\n  <div className=\"flex items-center space-x-2\">\n    <RadioGroupItem value=\"option-one\" id=\"option-one\" />\n    <Label htmlFor=\"option-one\">Option One</Label>\n  </div>\n  <div className=\"flex items-center space-x-2\">\n    <RadioGroupItem value=\"option-two\" id=\"option-two\" />\n    <Label htmlFor=\"option-two\">Option Two</Label>\n  </div>\n</RadioGroup>"
        }
      ],
      "examples": [
        {
          "source": "radio-group-demo.tsx",
          "code": "import { Label } from \"@/components/ui/label\"\r\nimport { RadioGroup, RadioGroupItem } from \"@/components/ui/radio-group\"\r\n\r\nexport default function RadioGroupDemo() {\r\n  return (\r\n    <RadioGroup defaultValue=\"comfortable\">\r\n      <div className=\"flex items-center space-x-2\">\r\n        <RadioGroupItem value=\"default\" id=\"r1\" />\r\n        <Label htmlFor=\"r1\">Default</Label>\r\n      </div>\r\n      <div className=\"flex items-center space-x-2\">\r\n        <RadioGroupItem value=\"comfortable\" id=\"r2\" />\r\n        <Label htmlFor=\"r2\">Comfortable</Label>\r\n      </div>\r\n      <div className=\"flex items-center space-x-2\">\r\n        <RadioGroupItem value=\"compact\" id=\"r3\" />\r\n        <Label htmlFor=\"r3\">Compact</Label>\r\n      </div>\r\n    </RadioGroup>\r\n  )\r\n}"
        }
      ]
    }
  },
  {
    "name": "Scroll Area",
    "description": "Augments native scroll functionality for custom, cross-browser styling.",
    "docs_path": "build\\gits\\shadcn-ui$ui-openv0remix\\docs\\scroll-area.mdx",
    "docs": {
      "import": {
        "source": "scroll-area.mdx",
        "code": "import { ScrollArea } from \"@/components/ui/scroll-area\""
      },
      "use": [
        {
          "source": "scroll-area.mdx",
          "code": "<ScrollArea className=\"h-[200px] w-[350px] rounded-md border p-4\">\n  Jokester began sneaking into the castle in the middle of the night and leaving\n  jokes all over the place: under the king's pillow, in his soup, even in the\n  royal toilet. The king was furious, but he couldn't seem to stop Jokester. And\n  then, one day, the people of the kingdom discovered that the jokes left by\n  Jokester were so funny that they couldn't help but laugh. And once they\n  started laughing, they couldn't stop.\n</ScrollArea>"
        }
      ],
      "examples": [
        {
          "source": "scroll-area-demo.tsx",
          "code": "import * as React from \"react\"\r\n\r\nimport { ScrollArea } from \"@/components/ui/scroll-area\"\r\nimport { Separator } from \"@/components/ui/separator\"\r\n\r\nconst tags = Array.from({ length: 50 }).map(\r\n  (_, i, a) => `v1.2.0-beta.${a.length - i}`\r\n)\r\n\r\nexport default function ScrollAreaDemo() {\r\n  return (\r\n    <ScrollArea className=\"h-72 w-48 rounded-md border\">\r\n      <div className=\"p-4\">\r\n        <h4 className=\"mb-4 text-sm font-medium leading-none\">Tags</h4>\r\n        {tags.map((tag) => (\r\n          <>\r\n            <div key={tag} className=\"text-sm\">\r\n              {tag}\r\n            </div>\r\n            <Separator className=\"my-2\" />\r\n          </>\r\n        ))}\r\n      </div>\r\n    </ScrollArea>\r\n  )\r\n}"
        }
      ]
    }
  },
  {
    "name": "Select",
    "description": "Displays a list of options for the user to pick from—triggered by a button.",
    "docs_path": "build\\gits\\shadcn-ui$ui-openv0remix\\docs\\select.mdx",
    "docs": {
      "import": {
        "source": "select.mdx",
        "code": "import {\n  Select,\n  SelectContent,\n  SelectItem,\n  SelectTrigger,\n  SelectValue,\n} from \"@/components/ui/select\""
      },
      "use": [
        {
          "source": "select.mdx",
          "code": "<Select>\n  <SelectTrigger className=\"w-[180px]\">\n    <SelectValue placeholder=\"Theme\" />\n  </SelectTrigger>\n  <SelectContent>\n    <SelectItem value=\"light\">Light</SelectItem>\n    <SelectItem value=\"dark\">Dark</SelectItem>\n    <SelectItem value=\"system\">System</SelectItem>\n  </SelectContent>\n</Select>"
        }
      ],
      "examples": [
        {
          "source": "select-demo.tsx",
          "code": "import * as React from \"react\"\r\n\r\nimport {\r\n  Select,\r\n  SelectContent,\r\n  SelectGroup,\r\n  SelectItem,\r\n  SelectLabel,\r\n  SelectTrigger,\r\n  SelectValue,\r\n} from \"@/components/ui/select\"\r\n\r\nexport default function SelectDemo() {\r\n  return (\r\n    <Select>\r\n      <SelectTrigger className=\"w-[180px]\">\r\n        <SelectValue placeholder=\"Select a fruit\" />\r\n      </SelectTrigger>\r\n      <SelectContent>\r\n        <SelectGroup>\r\n          <SelectLabel>Fruits</SelectLabel>\r\n          <SelectItem value=\"apple\">Apple</SelectItem>\r\n          <SelectItem value=\"banana\">Banana</SelectItem>\r\n          <SelectItem value=\"blueberry\">Blueberry</SelectItem>\r\n          <SelectItem value=\"grapes\">Grapes</SelectItem>\r\n          <SelectItem value=\"pineapple\">Pineapple</SelectItem>\r\n        </SelectGroup>\r\n      </SelectContent>\r\n    </Select>\r\n  )\r\n}"
        }
      ]
    }
  },
  {
    "name": "Separator",
    "description": "Visually or semantically separates content.",
    "docs_path": "build\\gits\\shadcn-ui$ui-openv0remix\\docs\\separator.mdx",
    "docs": {
      "import": {
        "source": "separator.mdx",
        "code": "import { Separator } from \"@/components/ui/separator\""
      },
      "use": [{ "source": "separator.mdx", "code": "<Separator />" }],
      "examples": [
        {
          "source": "separator-demo.tsx",
          "code": "import { Separator } from \"@/components/ui/separator\"\r\n\r\nexport default function SeparatorDemo() {\r\n  return (\r\n    <div>\r\n      <div className=\"space-y-1\">\r\n        <h4 className=\"text-sm font-medium leading-none\">Radix Primitives</h4>\r\n        <p className=\"text-sm text-muted-foreground\">\r\n          An open-source UI component library.\r\n        </p>\r\n      </div>\r\n      <Separator className=\"my-4\" />\r\n      <div className=\"flex h-5 items-center space-x-4 text-sm\">\r\n        <div>Blog</div>\r\n        <Separator orientation=\"vertical\" />\r\n        <div>Docs</div>\r\n        <Separator orientation=\"vertical\" />\r\n        <div>Source</div>\r\n      </div>\r\n    </div>\r\n  )\r\n}"
        }
      ]
    }
  },
  {
    "name": "Sheet",
    "description": "Extends the Dialog component to display content that complements the main content of the screen.",
    "docs_path": "build\\gits\\shadcn-ui$ui-openv0remix\\docs\\sheet.mdx",
    "docs": {
      "import": {
        "source": "sheet.mdx",
        "code": "import {\n  Sheet,\n  SheetContent,\n  SheetDescription,\n  SheetHeader,\n  SheetTitle,\n  SheetTrigger,\n} from \"@/components/ui/sheet\""
      },
      "use": [
        {
          "source": "sheet.mdx",
          "code": "<Sheet>\n  <SheetTrigger>Open</SheetTrigger>\n  <SheetContent>\n    <SheetHeader>\n      <SheetTitle>Are you sure absolutely sure?</SheetTitle>\n      <SheetDescription>\n        This action cannot be undone. This will permanently delete your account\n        and remove your data from our servers.\n      </SheetDescription>\n    </SheetHeader>\n  </SheetContent>\n</Sheet>"
        }
      ],
      "examples": [
        {
          "source": "sheet-demo.tsx",
          "code": "import { Button } from \"@/components/ui/button\"\r\nimport { Input } from \"@/components/ui/input\"\r\nimport { Label } from \"@/components/ui/label\"\r\nimport {\r\n  Sheet,\r\n  SheetClose,\r\n  SheetContent,\r\n  SheetDescription,\r\n  SheetFooter,\r\n  SheetHeader,\r\n  SheetTitle,\r\n  SheetTrigger,\r\n} from \"@/components/ui/sheet\"\r\n\r\nexport default function SheetDemo() {\r\n  return (\r\n    <Sheet>\r\n      <SheetTrigger asChild>\r\n        <Button variant=\"outline\">Open</Button>\r\n      </SheetTrigger>\r\n      <SheetContent>\r\n        <SheetHeader>\r\n          <SheetTitle>Edit profile</SheetTitle>\r\n          <SheetDescription>\r\n            Make changes to your profile here. Click save when you're done.\r\n          </SheetDescription>\r\n        </SheetHeader>\r\n        <div className=\"grid gap-4 py-4\">\r\n          <div className=\"grid grid-cols-4 items-center gap-4\">\r\n            <Label htmlFor=\"name\" className=\"text-right\">\r\n              Name\r\n            </Label>\r\n            <Input id=\"name\" value=\"Pedro Duarte\" className=\"col-span-3\" />\r\n          </div>\r\n          <div className=\"grid grid-cols-4 items-center gap-4\">\r\n            <Label htmlFor=\"username\" className=\"text-right\">\r\n              Username\r\n            </Label>\r\n            <Input id=\"username\" value=\"@peduarte\" className=\"col-span-3\" />\r\n          </div>\r\n        </div>\r\n        <SheetFooter>\r\n          <SheetClose asChild>\r\n            <Button type=\"submit\">Save changes</Button>\r\n          </SheetClose>\r\n        </SheetFooter>\r\n      </SheetContent>\r\n    </Sheet>\r\n  )\r\n}"
        }
      ]
    }
  },
  {
    "name": "Skeleton",
    "description": "Use to show a placeholder while content is loading.",
    "docs_path": "build\\gits\\shadcn-ui$ui-openv0remix\\docs\\skeleton.mdx",
    "docs": {
      "import": {
        "source": "skeleton.mdx",
        "code": "import { Skeleton } from \"@/components/ui/skeleton\""
      },
      "use": [
        {
          "source": "skeleton.mdx",
          "code": "<Skeleton className=\"w-[100px] h-[20px] rounded-full\" />"
        }
      ],
      "examples": [
        {
          "source": "skeleton-demo.tsx",
          "code": "import { Skeleton } from \"@/components/ui/skeleton\"\r\n\r\nexport default function SkeletonDemo() {\r\n  return (\r\n    <div className=\"flex items-center space-x-4\">\r\n      <Skeleton className=\"h-12 w-12 rounded-full\" />\r\n      <div className=\"space-y-2\">\r\n        <Skeleton className=\"h-4 w-[250px]\" />\r\n        <Skeleton className=\"h-4 w-[200px]\" />\r\n      </div>\r\n    </div>\r\n  )\r\n}"
        }
      ]
    }
  },
  {
    "name": "Slider",
    "description": "An input where the user selects a value from within a given range.",
    "docs_path": "build\\gits\\shadcn-ui$ui-openv0remix\\docs\\slider.mdx",
    "docs": {
      "import": {
        "source": "slider.mdx",
        "code": "import { Slider } from \"@/components/ui/slider\""
      },
      "use": [
        {
          "source": "slider.mdx",
          "code": "<Slider defaultValue={[33]} max={100} step={1} />"
        }
      ],
      "examples": [
        {
          "source": "slider-demo.tsx",
          "code": "import { cn } from \"@/lib/utils\"\r\nimport { Slider } from \"@/components/ui/slider\"\r\n\r\ntype SliderProps = React.ComponentProps<typeof Slider>\r\n\r\nexport default function SliderDemo({ className, ...props }: SliderProps) {\r\n  return (\r\n    <Slider\r\n      defaultValue={[50]}\r\n      max={100}\r\n      step={1}\r\n      className={cn(\"w-[60%]\", className)}\r\n      {...props}\r\n    />\r\n  )\r\n}"
        }
      ]
    }
  },
  {
    "name": "Switch",
    "description": "A control that allows the user to toggle between checked and not checked.",
    "docs_path": "build\\gits\\shadcn-ui$ui-openv0remix\\docs\\switch.mdx",
    "docs": {
      "import": {
        "source": "switch.mdx",
        "code": "import { Switch } from \"@/components/ui/switch\""
      },
      "use": [{ "source": "switch.mdx", "code": "<Switch />" }],
      "examples": [
        {
          "source": "switch-demo.tsx",
          "code": "import { Label } from \"@/components/ui/label\"\r\nimport { Switch } from \"@/components/ui/switch\"\r\n\r\nexport default function SwitchDemo() {\r\n  return (\r\n    <div className=\"flex items-center space-x-2\">\r\n      <Switch id=\"airplane-mode\" />\r\n      <Label htmlFor=\"airplane-mode\">Airplane Mode</Label>\r\n    </div>\r\n  )\r\n}"
        }
      ]
    }
  },
  {
    "name": "Table",
    "description": "A responsive table component.",
    "docs_path": "build\\gits\\shadcn-ui$ui-openv0remix\\docs\\table.mdx",
    "docs": {
      "import": {
        "source": "table.mdx",
        "code": "import {\n  Table,\n  TableBody,\n  TableCaption,\n  TableCell,\n  TableHead,\n  TableHeader,\n  TableRow,\n} from \"@/components/ui/table\""
      },
      "use": [
        {
          "source": "table.mdx",
          "code": "<Table>\n  <TableCaption>A list of your recent invoices.</TableCaption>\n  <TableHeader>\n    <TableRow>\n      <TableHead className=\"w-[100px]\">Invoice</TableHead>\n      <TableHead>Status</TableHead>\n      <TableHead>Method</TableHead>\n      <TableHead className=\"text-right\">Amount</TableHead>\n    </TableRow>\n  </TableHeader>\n  <TableBody>\n    <TableRow>\n      <TableCell className=\"font-medium\">INV001</TableCell>\n      <TableCell>Paid</TableCell>\n      <TableCell>Credit Card</TableCell>\n      <TableCell className=\"text-right\">$250.00</TableCell>\n    </TableRow>\n  </TableBody>\n</Table>"
        }
      ],
      "examples": [
        {
          "source": "table-demo.tsx",
          "code": "import {\r\n  Table,\r\n  TableBody,\r\n  TableCaption,\r\n  TableCell,\r\n  TableHead,\r\n  TableHeader,\r\n  TableRow,\r\n} from \"@/components/ui/table\"\r\n\r\nconst invoices = [\r\n  {\r\n    invoice: \"INV001\",\r\n    paymentStatus: \"Paid\",\r\n    totalAmount: \"$250.00\",\r\n    paymentMethod: \"Credit Card\",\r\n  },\r\n  {\r\n    invoice: \"INV002\",\r\n    paymentStatus: \"Pending\",\r\n    totalAmount: \"$150.00\",\r\n    paymentMethod: \"PayPal\",\r\n  },\r\n  {\r\n    invoice: \"INV003\",\r\n    paymentStatus: \"Unpaid\",\r\n    totalAmount: \"$350.00\",\r\n    paymentMethod: \"Bank Transfer\",\r\n  },\r\n  {\r\n    invoice: \"INV004\",\r\n    paymentStatus: \"Paid\",\r\n    totalAmount: \"$450.00\",\r\n    paymentMethod: \"Credit Card\",\r\n  },\r\n  {\r\n    invoice: \"INV005\",\r\n    paymentStatus: \"Paid\",\r\n    totalAmount: \"$550.00\",\r\n    paymentMethod: \"PayPal\",\r\n  },\r\n  {\r\n    invoice: \"INV006\",\r\n    paymentStatus: \"Pending\",\r\n    totalAmount: \"$200.00\",\r\n    paymentMethod: \"Bank Transfer\",\r\n  },\r\n  {\r\n    invoice: \"INV007\",\r\n    paymentStatus: \"Unpaid\",\r\n    totalAmount: \"$300.00\",\r\n    paymentMethod: \"Credit Card\",\r\n  },\r\n]\r\n\r\nexport default function TableDemo() {\r\n  return (\r\n    <Table>\r\n      <TableCaption>A list of your recent invoices.</TableCaption>\r\n      <TableHeader>\r\n        <TableRow>\r\n          <TableHead className=\"w-[100px]\">Invoice</TableHead>\r\n          <TableHead>Status</TableHead>\r\n          <TableHead>Method</TableHead>\r\n          <TableHead className=\"text-right\">Amount</TableHead>\r\n        </TableRow>\r\n      </TableHeader>\r\n      <TableBody>\r\n        {invoices.map((invoice) => (\r\n          <TableRow key={invoice.invoice}>\r\n            <TableCell className=\"font-medium\">{invoice.invoice}</TableCell>\r\n            <TableCell>{invoice.paymentStatus}</TableCell>\r\n            <TableCell>{invoice.paymentMethod}</TableCell>\r\n            <TableCell className=\"text-right\">{invoice.totalAmount}</TableCell>\r\n          </TableRow>\r\n        ))}\r\n      </TableBody>\r\n    </Table>\r\n  )\r\n}"
        }
      ]
    }
  },
  {
    "name": "Tabs",
    "description": "A set of layered sections of content—known as tab panels—that are displayed one at a time.",
    "docs_path": "build\\gits\\shadcn-ui$ui-openv0remix\\docs\\tabs.mdx",
    "docs": {
      "import": {
        "source": "tabs.mdx",
        "code": "import { Tabs, TabsContent, TabsList, TabsTrigger } from \"@/components/ui/tabs\""
      },
      "use": [
        {
          "source": "tabs.mdx",
          "code": "<Tabs defaultValue=\"account\" className=\"w-[400px]\">\n  <TabsList>\n    <TabsTrigger value=\"account\">Account</TabsTrigger>\n    <TabsTrigger value=\"password\">Password</TabsTrigger>\n  </TabsList>\n  <TabsContent value=\"account\">Make changes to your account here.</TabsContent>\n  <TabsContent value=\"password\">Change your password here.</TabsContent>\n</Tabs>"
        }
      ],
      "examples": [
        {
          "source": "tabs-demo.tsx",
          "code": "import { Button } from \"@/components/ui/button\"\r\nimport {\r\n  Card,\r\n  CardContent,\r\n  CardDescription,\r\n  CardFooter,\r\n  CardHeader,\r\n  CardTitle,\r\n} from \"@/components/ui/card\"\r\nimport { Input } from \"@/components/ui/input\"\r\nimport { Label } from \"@/components/ui/label\"\r\nimport {\r\n  Tabs,\r\n  TabsContent,\r\n  TabsList,\r\n  TabsTrigger,\r\n} from \"@/components/ui/tabs\"\r\n\r\nexport default function TabsDemo() {\r\n  return (\r\n    <Tabs defaultValue=\"account\" className=\"w-[400px]\">\r\n      <TabsList className=\"grid w-full grid-cols-2\">\r\n        <TabsTrigger value=\"account\">Account</TabsTrigger>\r\n        <TabsTrigger value=\"password\">Password</TabsTrigger>\r\n      </TabsList>\r\n      <TabsContent value=\"account\">\r\n        <Card>\r\n          <CardHeader>\r\n            <CardTitle>Account</CardTitle>\r\n            <CardDescription>\r\n              Make changes to your account here. Click save when you're done.\r\n            </CardDescription>\r\n          </CardHeader>\r\n          <CardContent className=\"space-y-2\">\r\n            <div className=\"space-y-1\">\r\n              <Label htmlFor=\"name\">Name</Label>\r\n              <Input id=\"name\" defaultValue=\"Pedro Duarte\" />\r\n            </div>\r\n            <div className=\"space-y-1\">\r\n              <Label htmlFor=\"username\">Username</Label>\r\n              <Input id=\"username\" defaultValue=\"@peduarte\" />\r\n            </div>\r\n          </CardContent>\r\n          <CardFooter>\r\n            <Button>Save changes</Button>\r\n          </CardFooter>\r\n        </Card>\r\n      </TabsContent>\r\n      <TabsContent value=\"password\">\r\n        <Card>\r\n          <CardHeader>\r\n            <CardTitle>Password</CardTitle>\r\n            <CardDescription>\r\n              Change your password here. After saving, you'll be logged out.\r\n            </CardDescription>\r\n          </CardHeader>\r\n          <CardContent className=\"space-y-2\">\r\n            <div className=\"space-y-1\">\r\n              <Label htmlFor=\"current\">Current password</Label>\r\n              <Input id=\"current\" type=\"password\" />\r\n            </div>\r\n            <div className=\"space-y-1\">\r\n              <Label htmlFor=\"new\">New password</Label>\r\n              <Input id=\"new\" type=\"password\" />\r\n            </div>\r\n          </CardContent>\r\n          <CardFooter>\r\n            <Button>Save password</Button>\r\n          </CardFooter>\r\n        </Card>\r\n      </TabsContent>\r\n    </Tabs>\r\n  )\r\n}"
        }
      ]
    }
  },
  {
    "name": "Textarea",
    "description": "Displays a form textarea or a component that looks like a textarea.",
    "docs_path": "build\\gits\\shadcn-ui$ui-openv0remix\\docs\\textarea.mdx",
    "docs": {
      "import": {
        "source": "textarea.mdx",
        "code": "import { Textarea } from \"@/components/ui/textarea\""
      },
      "use": [{ "source": "textarea.mdx", "code": "<Textarea />" }],
      "examples": [
        {
          "source": "textarea-demo.tsx",
          "code": "import { Textarea } from \"@/components/ui/textarea\"\r\n\r\nexport default function TextareaDemo() {\r\n  return <Textarea placeholder=\"Type your message here.\" />\r\n}"
        },
        {
          "source": "textarea-disabled.tsx",
          "code": "import { Textarea } from \"@/components/ui/textarea\"\r\n\r\nexport default function TextareaDisabled() {\r\n  return <Textarea placeholder=\"Type your message here.\" disabled />\r\n}"
        },
        {
          "source": "textarea-with-button.tsx",
          "code": "import { Button } from \"@/components/ui/button\"\r\nimport { Textarea } from \"@/components/ui/textarea\"\r\n\r\nexport default function TextareaWithButton() {\r\n  return (\r\n    <div className=\"grid w-full gap-2\">\r\n      <Textarea placeholder=\"Type your message here.\" />\r\n      <Button>Send message</Button>\r\n    </div>\r\n  )\r\n}"
        },
        {
          "source": "textarea-with-label.tsx",
          "code": "import { Label } from \"@/components/ui/label\"\r\nimport { Textarea } from \"@/components/ui/textarea\"\r\n\r\nexport default function TextareaWithLabel() {\r\n  return (\r\n    <div className=\"grid w-full gap-1.5\">\r\n      <Label htmlFor=\"message\">Your message</Label>\r\n      <Textarea placeholder=\"Type your message here.\" id=\"message\" />\r\n    </div>\r\n  )\r\n}"
        },
        {
          "source": "textarea-with-text.tsx",
          "code": "import { Label } from \"@/components/ui/label\"\r\nimport { Textarea } from \"@/components/ui/textarea\"\r\n\r\nexport default function TextareaWithText() {\r\n  return (\r\n    <div className=\"grid w-full gap-1.5\">\r\n      <Label htmlFor=\"message-2\">Your Message</Label>\r\n      <Textarea placeholder=\"Type your message here.\" id=\"message-2\" />\r\n      <p className=\"text-sm text-muted-foreground\">\r\n        Your message will be copied to the support team.\r\n      </p>\r\n    </div>\r\n  )\r\n}"
        }
      ]
    }
  },
  {
    "name": "Toast",
    "description": "A succinct message that is displayed temporarily.",
    "docs_path": "build\\gits\\shadcn-ui$ui-openv0remix\\docs\\toast.mdx",
    "docs": {
      "import": {
        "source": "toast.mdx",
        "code": "import { useToast } from \"@/components/ui/use-toast\""
      },
      "use": [],
      "examples": [
        {
          "source": "toast-demo.tsx",
          "code": "\"use client\"\r\n\r\nimport { Button } from \"@/components/ui/button\"\r\nimport { ToastAction } from \"@/components/ui/toast\"\r\nimport { useToast } from \"@/components/ui/use-toast\"\r\n\r\nexport default function ToastDemo() {\r\n  const { toast } = useToast()\r\n\r\n  return (\r\n    <Button\r\n      variant=\"outline\"\r\n      onClick={() => {\r\n        toast({\r\n          title: \"Scheduled: Catch up \",\r\n          description: \"Friday, February 10, 2023 at 5:57 PM\",\r\n          action: (\r\n            <ToastAction altText=\"Goto schedule to undo\">Undo</ToastAction>\r\n          ),\r\n        })\r\n      }}\r\n    >\r\n      Add to calendar\r\n    </Button>\r\n  )\r\n}"
        },
        {
          "source": "toast-destructive.tsx",
          "code": "\"use client\"\r\n\r\nimport { Button } from \"@/components/ui/button\"\r\nimport { ToastAction } from \"@/components/ui/toast\"\r\nimport { useToast } from \"@/components/ui/use-toast\"\r\n\r\nexport default function ToastDestructive() {\r\n  const { toast } = useToast()\r\n\r\n  return (\r\n    <Button\r\n      variant=\"outline\"\r\n      onClick={() => {\r\n        toast({\r\n          variant: \"destructive\",\r\n          title: \"Uh oh! Something went wrong.\",\r\n          description: \"There was a problem with your request.\",\r\n          action: <ToastAction altText=\"Try again\">Try again</ToastAction>,\r\n        })\r\n      }}\r\n    >\r\n      Show Toast\r\n    </Button>\r\n  )\r\n}"
        },
        {
          "source": "toast-simple.tsx",
          "code": "\"use client\"\r\n\r\nimport { Button } from \"@/components/ui/button\"\r\nimport { useToast } from \"@/components/ui/use-toast\"\r\n\r\nexport default function ToastSimple() {\r\n  const { toast } = useToast()\r\n\r\n  return (\r\n    <Button\r\n      variant=\"outline\"\r\n      onClick={() => {\r\n        toast({\r\n          description: \"Your message has been sent.\",\r\n        })\r\n      }}\r\n    >\r\n      Show Toast\r\n    </Button>\r\n  )\r\n}"
        },
        {
          "source": "toast-with-action.tsx",
          "code": "\"use client\"\r\n\r\nimport { Button } from \"@/components/ui/button\"\r\nimport { ToastAction } from \"@/components/ui/toast\"\r\nimport { useToast } from \"@/components/ui/use-toast\"\r\n\r\nexport default function ToastWithAction() {\r\n  const { toast } = useToast()\r\n\r\n  return (\r\n    <Button\r\n      variant=\"outline\"\r\n      onClick={() => {\r\n        toast({\r\n          title: \"Uh oh! Something went wrong.\",\r\n          description: \"There was a problem with your request.\",\r\n          action: <ToastAction altText=\"Try again\">Try again</ToastAction>,\r\n        })\r\n      }}\r\n    >\r\n      Show Toast\r\n    </Button>\r\n  )\r\n}"
        },
        {
          "source": "toast-with-title.tsx",
          "code": "\"use client\"\r\n\r\nimport { Button } from \"@/components/ui/button\"\r\nimport { useToast } from \"@/components/ui/use-toast\"\r\n\r\nexport default function ToastWithTitle() {\r\n  const { toast } = useToast()\r\n\r\n  return (\r\n    <Button\r\n      variant=\"outline\"\r\n      onClick={() => {\r\n        toast({\r\n          title: \"Uh oh! Something went wrong.\",\r\n          description: \"There was a problem with your request.\",\r\n        })\r\n      }}\r\n    >\r\n      Show Toast\r\n    </Button>\r\n  )\r\n}"
        }
      ]
    }
  },
  {
    "name": "Toggle",
    "description": "A two-state button that can be either on or off.",
    "docs_path": "build\\gits\\shadcn-ui$ui-openv0remix\\docs\\toggle.mdx",
    "docs": {
      "import": {
        "source": "toggle.mdx",
        "code": "import { Toggle } from \"@/components/ui/toggle\""
      },
      "use": [{ "source": "toggle.mdx", "code": "<Toggle>Toggle</Toggle>" }],
      "examples": [
        {
          "source": "toggle-demo.tsx",
          "code": "import { Bold } from \"lucide-react\"\r\n\r\nimport { Toggle } from \"@/components/ui/toggle\"\r\n\r\nexport default function ToggleDemo() {\r\n  return (\r\n    <Toggle aria-label=\"Toggle italic\">\r\n      <Bold className=\"h-4 w-4\" />\r\n    </Toggle>\r\n  )\r\n}"
        },
        {
          "source": "toggle-disabled.tsx",
          "code": "import { Underline } from \"lucide-react\"\r\n\r\nimport { Toggle } from \"@/components/ui/toggle\"\r\n\r\nexport default function ToggleDisabled() {\r\n  return (\r\n    <Toggle aria-label=\"Toggle italic\" disabled>\r\n      <Underline className=\"h-4 w-4\" />\r\n    </Toggle>\r\n  )\r\n}"
        },
        {
          "source": "toggle-lg.tsx",
          "code": "import { Italic } from \"lucide-react\"\r\n\r\nimport { Toggle } from \"@/components/ui/toggle\"\r\n\r\nexport default function ToggleLg() {\r\n  return (\r\n    <Toggle size=\"lg\" aria-label=\"Toggle italic\">\r\n      <Italic className=\"h-4 w-4\" />\r\n    </Toggle>\r\n  )\r\n}"
        },
        {
          "source": "toggle-outline.tsx",
          "code": "import { Italic } from \"lucide-react\"\r\n\r\nimport { Toggle } from \"@/components/ui/toggle\"\r\n\r\nexport default function ToggleOutline() {\r\n  return (\r\n    <Toggle variant=\"outline\" aria-label=\"Toggle italic\">\r\n      <Italic className=\"h-4 w-4\" />\r\n    </Toggle>\r\n  )\r\n}"
        },
        {
          "source": "toggle-sm.tsx",
          "code": "import { Italic } from \"lucide-react\"\r\n\r\nimport { Toggle } from \"@/components/ui/toggle\"\r\n\r\nexport default function ToggleSm() {\r\n  return (\r\n    <Toggle size=\"sm\" aria-label=\"Toggle italic\">\r\n      <Italic className=\"h-4 w-4\" />\r\n    </Toggle>\r\n  )\r\n}"
        },
        {
          "source": "toggle-with-text.tsx",
          "code": "import { Italic } from \"lucide-react\"\r\n\r\nimport { Toggle } from \"@/components/ui/toggle\"\r\n\r\nexport default function ToggleWithText() {\r\n  return (\r\n    <Toggle aria-label=\"Toggle italic\">\r\n      <Italic className=\"mr-2 h-4 w-4\" />\r\n      Italic\r\n    </Toggle>\r\n  )\r\n}"
        }
      ]
    }
  },
  {
    "name": "Tooltip",
    "description": "A popup that displays information related to an element when the element receives keyboard focus or the mouse hovers over it.",
    "docs_path": "build\\gits\\shadcn-ui$ui-openv0remix\\docs\\tooltip.mdx",
    "docs": {
      "import": {
        "source": "tooltip.mdx",
        "code": "import {\n  Tooltip,\n  TooltipContent,\n  TooltipProvider,\n  TooltipTrigger,\n} from \"@/components/ui/tooltip\""
      },
      "use": [
        {
          "source": "tooltip.mdx",
          "code": "<TooltipProvider>\n  <Tooltip>\n    <TooltipTrigger>Hover</TooltipTrigger>\n    <TooltipContent>\n      <p>Add to library</p>\n    </TooltipContent>\n  </Tooltip>\n</TooltipProvider>"
        }
      ],
      "examples": [
        {
          "source": "tooltip-demo.tsx",
          "code": "import { Button } from \"@/components/ui/button\"\r\nimport {\r\n  Tooltip,\r\n  TooltipContent,\r\n  TooltipProvider,\r\n  TooltipTrigger,\r\n} from \"@/components/ui/tooltip\"\r\n\r\nexport default function TooltipDemo() {\r\n  return (\r\n    <TooltipProvider>\r\n      <Tooltip>\r\n        <TooltipTrigger asChild>\r\n          <Button variant=\"outline\">Hover</Button>\r\n        </TooltipTrigger>\r\n        <TooltipContent>\r\n          <p>Add to library</p>\r\n        </TooltipContent>\r\n      </Tooltip>\r\n    </TooltipProvider>\r\n  )\r\n}"
        }
      ]
    }
  }
]

```